#!/usr/bin/env python3
"""Generate SmarterPlaylists program JSON files from the local templates.

This script is LOCAL ONLY. It does not call Spotify or SmarterPlaylists.
It writes JSON files under programs/ so they can be reviewed and imported later.

Usage:
  python tools/generate_programs.py                 # 21 pool programs + 4 samples
  python tools/generate_programs.py --mode all      # 21 pool programs + 120 generators
  python tools/generate_programs.py --mode pools-only

Outputs:
  programs/pools/*.json
  programs/generated/*.json
  programs/manifest.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
TEMPLATES_DIR = ROOT / "templates"
DEFAULT_OUTDIR = ROOT / "programs"

PLACEHOLDER_RE = re.compile(r"__[A-Z0-9_]+__")


# ---------------------------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_text(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig") as handle:
        return handle.read()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Placeholder replacement
# ---------------------------------------------------------------------------

def replace_placeholders(obj: Any, mapping: dict[str, Any]) -> Any:
    """Recursively replace __PLACEHOLDER__ tokens.

    An exact string match returns the mapped value with its original type
    (important for integer and boolean node params). A substring match
    stringifies the value.
    """
    if isinstance(obj, dict):
        return {key: replace_placeholders(value, mapping) for key, value in obj.items()}
    if isinstance(obj, list):
        return [replace_placeholders(value, mapping) for value in obj]
    if isinstance(obj, str):
        if obj in mapping:
            return mapping[obj]

        def repl(match: re.Match[str]) -> str:
            key = match.group(0)
            if key not in mapping:
                return key
            value = mapping[key]
            if isinstance(value, bool):
                return "true" if value else "false"
            return str(value)

        return PLACEHOLDER_RE.sub(repl, obj)
    return obj


def collect_unresolved(obj: Any, found: set[str] | None = None) -> set[str]:
    if found is None:
        found = set()
    if isinstance(obj, dict):
        for value in obj.values():
            collect_unresolved(value, found)
    elif isinstance(obj, list):
        for value in obj:
            collect_unresolved(value, found)
    elif isinstance(obj, str):
        for match in PLACEHOLDER_RE.finditer(obj):
            found.add(match.group(0))
    return found


# ---------------------------------------------------------------------------
# Graph editing
# ---------------------------------------------------------------------------

def bypass_node(program: dict[str, Any], node_id: str) -> bool:
    """Remove a one-input filter node and reconnect its downstream consumers."""
    components = program.get("components", {})
    if node_id not in components:
        return False
    node = components[node_id]
    upstream = list(node.get("sources", {}).get("green", []))
    for component_id, component in components.items():
        if component_id == node_id:
            continue
        for refs in component.get("sources", {}).values():
            if node_id in refs:
                index = refs.index(node_id)
                refs[index:index + 1] = upstream
    del components[node_id]
    program.get("_positions", {}).pop(node_id, None)
    return True


def remove_node(program: dict[str, Any], node_id: str) -> bool:
    """Remove a node and every reference to it."""
    components = program.get("components", {})
    if node_id not in components:
        return False
    del components[node_id]
    program.get("_positions", {}).pop(node_id, None)
    for component in components.values():
        for refs in component.get("sources", {}).values():
            while node_id in refs:
                refs.remove(node_id)
    return True


def prune_empty_sources(program: dict[str, Any]) -> list[str]:
    """Remove tag/description/radio source nodes that have empty required params."""
    components = program.get("components", {})
    pool = components.get("pool")
    if not pool:
        return []
    refs = pool.get("sources", {}).get("green", [])
    removed: list[str] = []
    for ref in list(refs):
        component = components.get(ref)
        if not component:
            refs.remove(ref)
            continue
        component_type = component.get("type")
        params = component.get("params", {})
        is_empty = False
        if component_type == "LastFmTagTopTracks" and not str(params.get("tag", "")).strip():
            is_empty = True
        elif component_type == "TracksByDescription" and not str(params.get("description", "")).strip():
            is_empty = True
        elif component_type == "SpotifyArtistRadio" and not (
            str(params.get("uri", "")).strip() or str(params.get("name", "")).strip()
        ):
            is_empty = True
        if is_empty:
            refs.remove(ref)
            remove_node(program, ref)
            removed.append(ref)
    return removed


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_program(program: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    components = program.get("components")
    if not isinstance(components, dict) or not components:
        errors.append("program has no components")
        return errors, warnings

    main = program.get("main")
    if main not in components:
        errors.append(f"main node {main!r} not found")

    for component_id, component in components.items():
        if not isinstance(component, dict):
            errors.append(f"{component_id}: component is not an object")
            continue
        if "type" not in component:
            errors.append(f"{component_id}: missing type")
        sources = component.get("sources", {})
        if not isinstance(sources, dict):
            errors.append(f"{component_id}: sources is not an object")
            continue
        for port, refs in sources.items():
            if not isinstance(refs, list):
                errors.append(f"{component_id}.{port}: sources must be a list")
                continue
            for ref in refs:
                if ref not in components:
                    errors.append(f"{component_id}.{port}: missing upstream node {ref!r}")

    unresolved = collect_unresolved(program)
    if unresolved:
        errors.append(f"unresolved placeholders: {', '.join(sorted(unresolved))}")

    positions = program.get("_positions")
    if positions is not None:
        if not isinstance(positions, dict):
            errors.append("_positions is not an object")
        elif set(positions) != set(components):
            missing = sorted(set(components) - set(positions))
            extra = sorted(set(positions) - set(components))
            errors.append(f"_positions mismatch (missing={missing}, extra={extra})")

    if main in components:
        reachable: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in reachable or node_id not in components:
                return
            reachable.add(node_id)
            for refs in components[node_id].get("sources", {}).values():
                for ref in refs:
                    visit(ref)

        visit(main)
        for component_id, component in components.items():
            if component.get("type") != "comment" and component_id not in reachable:
                warnings.append(f"unreachable non-comment node: {component_id}")

    # Cycle check (only meaningful on the reachable graph, but check all).
    visiting: set[str] = set()
    visited: set[str] = set()

    def check_cycle(node_id: str) -> None:
        if node_id in visited or node_id not in components:
            return
        if node_id in visiting:
            errors.append(f"cycle detected at {node_id!r}")
            return
        visiting.add(node_id)
        for refs in components[node_id].get("sources", {}).values():
            for ref in refs:
                check_cycle(ref)
        visiting.discard(node_id)
        visited.add(node_id)

    for component_id in components:
        check_cycle(component_id)

    for component_id, component in components.items():
        if component.get("type") == "SpotifyPlaylist":
            uri = str(component.get("params", {}).get("uri", ""))
            if "REPLACE_ME" in uri:
                warnings.append(f"{component_id}: placeholder playlist URI")

    return errors, warnings


# ---------------------------------------------------------------------------
# Program builders
# ---------------------------------------------------------------------------

def build_priority_pool(
    pool: dict[str, Any],
    rules: dict[str, Any],
    template: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    track_uris = str(pool.get("priority_track_uris_text", "")).strip()
    if not track_uris:
        raise ValueError("Priority pool has no track URIs")

    mapping = {
        "__POOL_PROGRAM_NAME__": pool["program_name"],
        "__POOL_COMMENT__": pool["comment"],
        "__PRIORITY_TRACK_URIS__": track_uris,
        "__MIN_DURATION_MS__": pool.get("min_duration_ms", rules["min_duration_ms"]),
        "__MAX_DURATION_MS__": pool.get("max_duration_ms", rules["max_duration_ms"]),
        "__EXCLUDE_PATTERNS_REGEX__": pool.get("exclude_patterns_regex", rules["exclude_patterns_regex"]),
    }
    program = replace_placeholders(template, mapping)

    if not rules.get("exclude_short_tracks", False):
        bypass_node(program, "dur")
    if not rules.get("exclude_patterns", False) or not str(mapping["__EXCLUDE_PATTERNS_REGEX__"]).strip():
        bypass_node(program, "clean")

    errors, warnings = validate_program(program)
    if errors:
        raise ValueError("Priority pool validation failed: " + "; ".join(errors))
    return program, warnings


def build_genre_pool(
    pool: dict[str, Any],
    rules: dict[str, Any],
    template: dict[str, Any],
    series_uris_text: str,
) -> tuple[dict[str, Any], list[str]]:
    tags = list(pool.get("tags", []))
    descriptions = list(pool.get("descriptions", []))
    seeds = list(pool.get("radio_seeds", []))
    while len(tags) < 3:
        tags.append("")
    while len(descriptions) < 2:
        descriptions.append("")
    while len(seeds) < 3:
        seeds.append({"name": "", "uri": ""})

    base = pool.get("base_ranges", {})
    priority_names = str(pool.get("priority_artist_names_text", "")).strip()
    if not priority_names:
        raise ValueError(f"{pool['program_name']} has no priority artist names for SimpleArtistFilter")

    mapping = {
        "__POOL_PROGRAM_NAME__": pool["program_name"],
        "__POOL_COMMENT__": pool["comment"],
        "__TAG_1__": tags[0],
        "__TAG_2__": tags[1],
        "__TAG_3__": tags[2],
        "__TAG_LIMIT__": pool.get("tag_limit", rules["tag_limit"]),
        "__GENRE_FILTER__": pool.get("genre_filter", ""),
        "__ARTIST_GENRE__": pool.get("artist_genre", ""),
        "__GENRE_ARTISTS_COUNT__": pool.get("genre_artists_count", rules["genre_artists_count"]),
        "__GENRE_TRACKS_PER_ARTIST__": pool.get("genre_tracks_per_artist", rules["genre_tracks_per_artist"]),
        "__DESC_1__": descriptions[0],
        "__DESC_2__": descriptions[1],
        "__DESC_LIMIT__": pool.get("description_limit", rules["description_limit"]),
        "__RADIO_SEED_URI_1__": seeds[0].get("uri", ""),
        "__RADIO_SEED_NAME_1__": seeds[0].get("name", ""),
        "__RADIO_SEED_URI_2__": seeds[1].get("uri", ""),
        "__RADIO_SEED_NAME_2__": seeds[1].get("name", ""),
        "__RADIO_SEED_URI_3__": seeds[2].get("uri", ""),
        "__RADIO_SEED_NAME_3__": seeds[2].get("name", ""),
        "__PRIORITY_ARTIST_NAMES__": priority_names,
        "__ENERGY_MIN__": base.get("energy", [0, 1])[0],
        "__ENERGY_MAX__": base.get("energy", [0, 1])[1],
        "__VALENCE_MIN__": base.get("valence", [0, 1])[0],
        "__VALENCE_MAX__": base.get("valence", [0, 1])[1],
        "__TEMPO_MIN__": base.get("tempo", [0, 200])[0],
        "__TEMPO_MAX__": base.get("tempo", [0, 200])[1],
        "__DANCE_MIN__": base.get("danceability", [0, 1])[0],
        "__DANCE_MAX__": base.get("danceability", [0, 1])[1],
        "__ACOUSTIC_MIN__": base.get("acousticness", [0, 1])[0],
        "__ACOUSTIC_MAX__": base.get("acousticness", [0, 1])[1],
        "__POOL_SIZE__": pool.get("pool_size", rules["pool_size"]),
        "__GLOBAL_MAX_PER_ARTIST__": rules["global_max_per_artist"],
        "__MIN_DURATION_MS__": rules["min_duration_ms"],
        "__MAX_DURATION_MS__": rules["max_duration_ms"],
        "__EXCLUDE_PATTERNS_REGEX__": rules["exclude_patterns_regex"],
        "__SERIES_EXCLUSION_URIS__": series_uris_text,
    }
    program = replace_placeholders(template, mapping)

    # No MusicBrainz genre source if there is no artist genre.
    if not str(mapping["__ARTIST_GENRE__"]).strip():
        remove_node(program, "genre_tracks")
        remove_node(program, "genre_artists")

    # Explicit policy.
    if pool.get("explicit_mode") != "clean":
        bypass_node(program, "explicit")

    # Title pattern exclusion.
    if not rules.get("exclude_patterns", False) or not str(mapping["__EXCLUDE_PATTERNS_REGEX__"]).strip():
        bypass_node(program, "clean_titles")

    # Series exclusion.
    if not rules.get("exclude_series_tracks", False) or not series_uris_text.strip():
        bypass_node(program, "fresh")
        remove_node(program, "used_series")

    # Hard genre filter (the artist genre may still be present).
    if not str(mapping["__GENRE_FILTER__"]).strip():
        bypass_node(program, "genre_filter")

    # Duration filter.
    if not rules.get("exclude_short_tracks", False):
        bypass_node(program, "dur")

    prune_empty_sources(program)

    errors, warnings = validate_program(program)
    if errors:
        raise ValueError(f"{pool['program_name']} validation failed: " + "; ".join(errors))
    return program, warnings


def build_generator(
    playlist: dict[str, Any],
    template: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    energy = playlist["energy_range"]
    valence = playlist["valence_range"]
    tempo = playlist["tempo_range"]
    dance = playlist["danceability_range"]
    acoustic = playlist["acousticness_range"]

    mapping = {
        "__PLAYLIST_NAME__": playlist["name"],
        "__PLAYLIST_DESCRIPTION__": playlist["description"],
        "__PLAYLIST_COMMENT__": playlist["comment"],
        "__PRIORITY_POOL_URI__": playlist["priority_pool_playlist_uri"],
        "__GLOBAL_POOL_URI__": playlist["pool_playlist_uri"],
        "__GLOBAL_POOL_NAME__": playlist["pool_program_name"],
        "__PRIORITY_OFFSET__": playlist["priority_offset"],
        "__GLOBAL_OFFSET__": playlist["global_offset"],
        "__PRIORITY_SLICE__": playlist["priority_slice"],
        "__GLOBAL_SLICE__": playlist["global_slice"],
        "__PRIORITY_MAX_PER_ARTIST__": playlist["priority_max_per_artist"],
        "__GLOBAL_MAX_PER_ARTIST__": playlist["global_max_per_artist"],
        "__PRIORITY_SHARE__": playlist["priority_share"],
        "__GLOBAL_SHARE__": playlist["global_share"],
        "__EL_UTAMA_WEIGHT__": playlist["el_utama_weight"],
        "__GENRE_MATCH_VALUE__": playlist.get("genre_match_value", playlist["genre_filter"]),
        "__GENRE_MATCH_WEIGHT__": playlist["genre_match_weight"],
        "__ENERGY_MIN__": energy[0],
        "__ENERGY_MAX__": energy[1],
        "__VALENCE_MIN__": valence[0],
        "__VALENCE_MAX__": valence[1],
        "__TEMPO_MIN__": tempo[0],
        "__TEMPO_MAX__": tempo[1],
        "__DANCE_MIN__": dance[0],
        "__DANCE_MAX__": dance[1],
        "__ACOUSTIC_MIN__": acoustic[0],
        "__ACOUSTIC_MAX__": acoustic[1],
        "__MOS_LIMIT__": playlist["mos_limit"],
        "__CAP_SECONDS__": playlist["cap_seconds"],
    }
    program = replace_placeholders(template, mapping)

    if playlist["explicit_mode"] != "clean":
        bypass_node(program, "explicit")

    errors, warnings = validate_program(program)
    if errors:
        raise ValueError(f"{playlist['name']} validation failed: " + "; ".join(errors))
    return program, warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SmarterPlaylists program JSON locally.")
    parser.add_argument(
        "--mode",
        choices=["samples", "all", "pools-only"],
        default="samples",
        help="samples = 21 pools + 4 generator samples; all = 21 pools + 120 generators; pools-only = 21 pools",
    )
    parser.add_argument(
        "--outdir",
        default=str(DEFAULT_OUTDIR),
        help="Output directory (default: programs/)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing JSON files in outdir/pools and outdir/generated before generating",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = ROOT / outdir

    if args.clean:
        for subdir in ("pools", "generated"):
            directory = outdir / subdir
            if directory.exists():
                for old_file in directory.glob("*.json"):
                    old_file.unlink()

    rules = load_json(CONFIG_DIR / "rules.json")
    pool_manifest = load_json(CONFIG_DIR / "pool_manifest.json")
    playlists_doc = load_json(CONFIG_DIR / "playlists_120.draft.json")
    series_uris_text = " ".join(
        line.strip()
        for line in load_text(CONFIG_DIR / "series_exclusion_uris.txt").splitlines()
        if line.strip()
    )

    priority_template = load_json(TEMPLATES_DIR / "TEMPLATE_POOL_PRIORITY.json")
    genre_template = load_json(TEMPLATES_DIR / "TEMPLATE_POOL_CATEGORY.json")
    generator_template = load_json(TEMPLATES_DIR / "TEMPLATE_GENERATOR_6H.json")

    pools = pool_manifest["pools"]
    playlists = playlists_doc["playlists"]

    manifest: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "note": "Generated locally. No SmarterPlaylists program or Spotify playlist was created.",
        "pools": [],
        "generators": [],
        "warnings": [],
    }

    # Pools
    for pool in pools:
        if pool["type"] == "priority":
            program, warnings = build_priority_pool(pool, rules, priority_template)
        else:
            program, warnings = build_genre_pool(pool, rules, genre_template, series_uris_text)

        slug = slugify(pool["program_name"])
        path = outdir / "pools" / f"{slug}.json"
        write_json(path, program)
        manifest["pools"].append(
            {
                "program_name": pool["program_name"],
                "type": pool["type"],
                "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                "pool_playlist_uri": pool.get("pool_playlist_uri", ""),
                "warnings": warnings,
            }
        )
        manifest["warnings"].extend(f"{pool['program_name']}: {warning}" for warning in warnings)

    # Generator programs
    if args.mode != "pools-only":
        if args.mode == "samples":
            selected: list[dict[str, Any]] = []
            seen_categories: set[str] = set()
            for playlist in playlists:
                if playlist["category"] not in seen_categories:
                    selected.append(playlist)
                    seen_categories.add(playlist["category"])
            selected_playlists = selected
        else:
            selected_playlists = playlists

        for playlist in selected_playlists:
            program, warnings = build_generator(playlist, generator_template)
            slug = playlist["slug"]
            path = outdir / "generated" / f"{slug}.json"
            write_json(path, program)
            manifest["generators"].append(
                {
                    "playlist_name": playlist["name"],
                    "category": playlist["category"],
                    "genre": playlist["genre"],
                    "mood": playlist["mood"],
                    "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                    "priority_offset": playlist["priority_offset"],
                    "global_offset": playlist["global_offset"],
                    "warnings": warnings,
                }
            )
            manifest["warnings"].extend(f"{playlist['name']}: {warning}" for warning in warnings)

    manifest_path = outdir / "manifest.json"
    write_json(manifest_path, manifest)

    summary = {
        "mode": args.mode,
        "outdir": str(outdir),
        "pools_written": len(manifest["pools"]),
        "generators_written": len(manifest["generators"]),
        "warning_count": len(manifest["warnings"]),
        "manifest": str(manifest_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if manifest["warnings"]:
        print("\nWarnings:")
        for warning in manifest["warnings"]:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
