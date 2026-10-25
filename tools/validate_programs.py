#!/usr/bin/env python3
"""Validate generated SmarterPlaylists program JSON files locally.

This script does not call Spotify or SmarterPlaylists.

Usage:
  python tools/validate_programs.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
PROGRAMS_DIR = ROOT / "programs"
TOOLS_DIR = ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from generate_programs import validate_program  # noqa: E402


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_pool(program: dict[str, Any], pool: dict[str, Any], rules: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = program.get("components", {})
    name = pool.get("program_name", program.get("name", ""))

    if pool.get("type") == "priority":
        require("tracks" in components, f"{name}: missing tracks source", errors)
        if "tracks" in components:
            source = components["tracks"]
            require(source.get("type") == "TrackSource", f"{name}: tracks must be TrackSource", errors)
            params = source.get("params", {})
            uris = str(params.get("uris", "")).split()
            expected = int(pool.get("pool_size", 0) or 0)
            require(
                len(uris) == expected,
                f"{name}: expected {expected} track URIs, got {len(uris)}",
                errors,
            )
            require(params.get("alias") == "priority", f"{name}: tracks alias must be priority", errors)
        require("artists" not in components, f"{name}: priority pool must not use artists source", errors)
        require("el" not in components, f"{name}: priority pool must not use eL Utama source", errors)
        if "sort_date" in components:
            params = components["sort_date"].get("params", {})
            require(params.get("attr") == "release_date", f"{name}: sort_date attr must be release_date", errors)
            require(params.get("reverse") is True, f"{name}: sort_date must be descending", errors)
        else:
            errors.append(f"{name}: missing sort_date")
        if "sort_pop" in components:
            params = components["sort_pop"].get("params", {})
            require(params.get("attr") == "popularity", f"{name}: sort_pop attr must be popularity", errors)
            require(params.get("reverse") is False, f"{name}: sort_pop must be ascending", errors)
        else:
            errors.append(f"{name}: missing sort_pop")
        require("fresh" not in components, f"{name}: priority pool must not use series exclusion", errors)
        require("used_series" not in components, f"{name}: priority pool must not use used_series", errors)
        return errors

    # Genre pool
    for index in range(1, 4):
        node_id = f"tag{index}"
        require(node_id in components, f"{name}: missing {node_id}", errors)
        if node_id in components:
            expected = pool.get("tags", [])[index - 1] if len(pool.get("tags", [])) >= index else ""
            actual = components[node_id].get("params", {}).get("tag", "")
            require(actual == expected, f"{name}: {node_id} tag mismatch ({actual!r} != {expected!r})", errors)

    if pool.get("artist_genre"):
        require("genre_artists" in components, f"{name}: missing genre_artists", errors)
        if "genre_artists" in components:
            actual = components["genre_artists"].get("params", {}).get("genre", "")
            require(actual == pool.get("artist_genre"), f"{name}: genre_artists genre mismatch", errors)
    else:
        require("genre_artists" not in components, f"{name}: unexpected genre_artists", errors)

    require("no_priority" in components, f"{name}: missing no_priority", errors)
    if "no_priority" in components:
        actual = components["no_priority"].get("params", {}).get("artistNames", "")
        require(actual == pool.get("priority_artist_names_text"), f"{name}: priority artist names mismatch", errors)

    if rules.get("exclude_series_tracks", False):
        require("used_series" in components, f"{name}: missing used_series", errors)
        require("fresh" in components, f"{name}: missing fresh filter", errors)
        if "used_series" in components:
            uri_count = len(str(components["used_series"].get("params", {}).get("uris", "")).split())
            require(uri_count > 0, f"{name}: used_series has no URIs", errors)
    else:
        require("fresh" not in components, f"{name}: unexpected fresh filter", errors)

    if pool.get("explicit_mode") == "clean":
        require("explicit" in components, f"{name}: clean pool must keep Explicit", errors)
        if "explicit" in components:
            require(
                components["explicit"].get("params", {}).get("explicit") is False,
                f"{name}: clean pool Explicit must be false",
                errors,
            )
    else:
        require("explicit" not in components, f"{name}: allow pool must bypass Explicit", errors)

    if pool.get("genre_filter"):
        require("genre_filter" in components, f"{name}: missing genre_filter", errors)
        if "genre_filter" in components:
            actual = components["genre_filter"].get("params", {}).get("genre", "")
            require(actual == pool.get("genre_filter"), f"{name}: genre_filter mismatch", errors)
    else:
        require("genre_filter" not in components, f"{name}: unexpected genre_filter", errors)

    if rules.get("exclude_patterns", False):
        require("clean_titles" in components, f"{name}: missing clean_titles", errors)
    else:
        require("clean_titles" not in components, f"{name}: unexpected clean_titles", errors)

    if rules.get("exclude_short_tracks", False):
        require("dur" in components, f"{name}: missing duration filter", errors)
    else:
        require("dur" not in components, f"{name}: unexpected duration filter", errors)

    if "first" in components:
        require(
            components["first"].get("params", {}).get("sample_size") == pool.get("pool_size"),
            f"{name}: First sample_size mismatch",
            errors,
        )
    else:
        errors.append(f"{name}: missing first")

    if "max_artist" in components:
        require(
            components["max_artist"].get("params", {}).get("max_tracks") == rules.get("global_max_per_artist"),
            f"{name}: MaxTracksPerArtist mismatch",
            errors,
        )
    else:
        errors.append(f"{name}: missing max_artist")

    return errors


def check_generator(program: dict[str, Any], playlist: dict[str, Any], rules: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = program.get("components", {})
    name = playlist.get("name", program.get("name", ""))

    require(program.get("main") == "save", f"{name}: main must be save", errors)
    require("cap" in components, f"{name}: missing cap", errors)
    if "cap" in components:
        require(
            components["cap"].get("params", {}).get("time") == 21600,
            f"{name}: ShorterThan must be 21600 seconds",
            errors,
        )
        require(components["cap"].get("sources", {}).get("green") == ["mos"], f"{name}: cap input must be mos", errors)

    require("save" in components, f"{name}: missing PlaylistSave", errors)
    if "save" in components:
        save = components["save"]
        params = save.get("params", {})
        require(save.get("type") == "PlaylistSave", f"{name}: save must be PlaylistSave", errors)
        require(params.get("playlist_name") == playlist.get("name"), f"{name}: PlaylistSave name mismatch", errors)
        require(
            params.get("description") == playlist.get("description"),
            f"{name}: PlaylistSave description mismatch",
            errors,
        )
        require(params.get("playlist_uri") == "", f"{name}: PlaylistSave URI must be blank", errors)
        require(params.get("append") is False, f"{name}: PlaylistSave append must be false", errors)
        require(params.get("no_dups") is True, f"{name}: PlaylistSave no_dups must be true", errors)
        require(
            save.get("sources", {}).get("green") == ["cap"],
            f"{name}: PlaylistSave input must be cap",
            errors,
        )

    require("mos" in components, f"{name}: missing mos", errors)
    if "mos" in components:
        mos = components["mos"]
        params = mos.get("params", {})
        objectives = params.get("objectives", [])
        require(params.get("limit") == playlist.get("mos_limit"), f"{name}: MOS limit mismatch", errors)
        require(len(objectives) == 14, f"{name}: expected 14 MOS objectives, got {len(objectives)}", errors)

        by_type: dict[str, list[dict[str, Any]]] = {}
        for objective in objectives:
            by_type.setdefault(objective.get("type", ""), []).append(objective)

        match_run = by_type.get("match-max-run", [])
        require(len(match_run) == 1, f"{name}: missing match-max-run objective", errors)
        if match_run:
            objective = match_run[0]
            require(objective.get("field") == "artist", f"{name}: match-max-run field must be artist", errors)
            require(objective.get("max_run") == 1, f"{name}: match-max-run max_run must be 1", errors)
            require(
                objective.get("weight") == "unbreakable",
                f"{name}: match-max-run weight must be unbreakable",
                errors,
            )

        distribution = by_type.get("distribution", [])
        require(len(distribution) == 1, f"{name}: missing distribution objective", errors)
        if distribution:
            values = distribution[0].get("values", "")
            require("priority(60%)" in values, f"{name}: distribution must include priority(60%)", errors)
            require("global(40%)" in values, f"{name}: distribution must include global(40%)", errors)

        match_el = by_type.get("match", [])
        require(len(match_el) == 1, f"{name}: missing eL Utama match objective", errors)
        if match_el:
            objective = match_el[0]
            require(objective.get("field") == "artist", f"{name}: eL Utama match field must be artist", errors)
            require(objective.get("value") == "eL Utama", f"{name}: eL Utama match value mismatch", errors)
            require(
                objective.get("weight") == playlist.get("el_utama_weight"),
                f"{name}: eL Utama weight mismatch",
                errors,
            )

        minimize = by_type.get("minimize", [])
        require(len(minimize) == 1, f"{name}: missing minimize popularity objective", errors)
        if minimize:
            require(minimize[0].get("field") == "popularity", f"{name}: minimize field must be popularity", errors)
            require(minimize[0].get("weight") == "highest", f"{name}: minimize weight must be highest", errors)

        maximize = by_type.get("maximize", [])
        require(len(maximize) == 1, f"{name}: missing maximize release_year objective", errors)
        if maximize:
            require(maximize[0].get("field") == "release_year", f"{name}: maximize field must be release_year", errors)

        max_match = by_type.get("max-match", [])
        require(len(max_match) == 1, f"{name}: missing max-match objective", errors)
        if max_match:
            objective = max_match[0]
            require(objective.get("field") == "artist", f"{name}: max-match field must be artist", errors)
            require(
                objective.get("max_count") == playlist.get("priority_max_per_artist"),
                f"{name}: max-match max_count mismatch",
                errors,
            )

        contains = by_type.get("contains", [])
        require(len(contains) == 1, f"{name}: missing contains genre objective", errors)
        if contains:
            objective = contains[0]
            require(objective.get("field") == "mb_genres", f"{name}: contains field must be mb_genres", errors)
            require(
                objective.get("value") == playlist.get("genre_match_value"),
                f"{name}: contains genre value mismatch",
                errors,
            )
            require(
                objective.get("weight") == playlist.get("genre_match_weight"),
                f"{name}: contains genre weight mismatch",
                errors,
            )

        ranges = {objective.get("field"): objective for objective in by_type.get("range", [])}
        for field, playlist_field in [
            ("energy", "energy_range"),
            ("valence", "valence_range"),
            ("tempo", "tempo_range"),
            ("danceability", "danceability_range"),
            ("acousticness", "acousticness_range"),
        ]:
            require(field in ranges, f"{name}: missing {field} range objective", errors)
            if field in ranges:
                expected = playlist.get(playlist_field, [])
                require(
                    ranges[field].get("min_val") == expected[0] and ranges[field].get("max_val") == expected[1],
                    f"{name}: {field} range mismatch",
                    errors,
                )

        variety = by_type.get("variety", [])
        require(len(variety) == 1, f"{name}: missing variety objective", errors)
        if variety:
            require(variety[0].get("field") == "mb_genres", f"{name}: variety field must be mb_genres", errors)

    for node_id in ["priority_pool", "global_pool"]:
        require(node_id in components, f"{name}: missing {node_id}", errors)
    if "priority_pool" in components:
        require(
            components["priority_pool"].get("params", {}).get("uri") == playlist.get("priority_pool_playlist_uri"),
            f"{name}: priority pool URI mismatch",
            errors,
        )
        require(
            components["priority_pool"].get("params", {}).get("name") == "POOL Priority",
            f"{name}: priority pool name mismatch",
            errors,
        )
    if "global_pool" in components:
        require(
            components["global_pool"].get("params", {}).get("uri") == playlist.get("pool_playlist_uri"),
            f"{name}: global pool URI mismatch",
            errors,
        )
        require(
            components["global_pool"].get("params", {}).get("name") == playlist.get("pool_program_name"),
            f"{name}: global pool name mismatch",
            errors,
        )

    for node_id, expected in [
        ("priority_rotate", playlist.get("priority_offset")),
        ("global_rotate", playlist.get("global_offset")),
        ("priority_slice", playlist.get("priority_slice")),
        ("global_slice", playlist.get("global_slice")),
        ("priority_max", playlist.get("priority_max_per_artist")),
        ("global_max", playlist.get("global_max_per_artist")),
    ]:
        require(node_id in components, f"{name}: missing {node_id}", errors)
        if node_id in components:
            param = "sample_size" if "rotate" in node_id or "slice" in node_id else "max_tracks"
            require(
                components[node_id].get("params", {}).get(param) == expected,
                f"{name}: {node_id}.{param} mismatch",
                errors,
            )

    if "priority_concat" in components:
        require(
            components["priority_concat"].get("sources", {}).get("green") == ["priority_dedup", "priority_dedup"],
            f"{name}: priority_concat must duplicate priority_dedup",
            errors,
        )
    if "global_concat" in components:
        require(
            components["global_concat"].get("sources", {}).get("green") == ["global_dedup", "global_dedup"],
            f"{name}: global_concat must duplicate global_dedup",
            errors,
        )
    if "combine" in components:
        require(
            components["combine"].get("sources", {}).get("green") == ["priority_max", "global_max"],
            f"{name}: combine inputs mismatch",
            errors,
        )

    if playlist.get("explicit_mode") == "clean":
        require("explicit" in components, f"{name}: clean playlist must keep Explicit", errors)
        if "explicit" in components:
            require(
                components["explicit"].get("params", {}).get("explicit") is False,
                f"{name}: clean Explicit must be false",
                errors,
            )
            require(
                components["mos"].get("sources", {}).get("green") == ["explicit"],
                f"{name}: MOS must read from explicit",
                errors,
            )
    else:
        require("explicit" not in components, f"{name}: allow playlist must bypass Explicit", errors)
        if "mos" in components:
            require(
                components["mos"].get("sources", {}).get("green") == ["dedup"],
                f"{name}: MOS must read from dedup",
                errors,
            )

    return errors


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    rules = load_json(CONFIG_DIR / "rules.json")
    pool_manifest = load_json(CONFIG_DIR / "pool_manifest.json")
    playlists_doc = load_json(CONFIG_DIR / "playlists_120.draft.json")
    pools_by_name = {pool["program_name"]: pool for pool in pool_manifest["pools"]}
    playlists_by_name = {playlist["name"]: playlist for playlist in playlists_doc["playlists"]}

    manifest_path = PROGRAMS_DIR / "manifest.json"
    if not manifest_path.exists():
        print("programs/manifest.json not found. Run tools/generate_programs.py first.")
        raise SystemExit(1)
    manifest = load_json(manifest_path)

    pool_files = sorted((PROGRAMS_DIR / "pools").glob("*.json"))
    generator_files = sorted((PROGRAMS_DIR / "generated").glob("*.json"))

    if len(pool_files) != 21:
        errors.append(f"expected 21 pool files, got {len(pool_files)}")
    expected_generators = 4 if manifest.get("mode") == "samples" else 120 if manifest.get("mode") == "all" else 0
    if expected_generators and len(generator_files) != expected_generators:
        errors.append(f"expected {expected_generators} generator files, got {len(generator_files)}")

    seen_pools: set[str] = set()
    for path in pool_files:
        program = load_json(path)
        name = program.get("name", "")
        if name not in pools_by_name:
            errors.append(f"{path.name}: unknown pool name {name!r}")
            continue
        seen_pools.add(name)
        graph_errors, graph_warnings = validate_program(program)
        errors.extend(f"{path.name}: {error}" for error in graph_errors)
        warnings.extend(f"{path.name}: {warning}" for warning in graph_warnings)
        errors.extend(check_pool(program, pools_by_name[name], rules))

    missing_pools = set(pools_by_name) - seen_pools
    if missing_pools:
        errors.append(f"missing pool programs: {sorted(missing_pools)}")

    seen_generators: set[str] = set()
    for path in generator_files:
        program = load_json(path)
        name = program.get("name", "")
        if name not in playlists_by_name:
            errors.append(f"{path.name}: unknown playlist name {name!r}")
            continue
        seen_generators.add(name)
        graph_errors, graph_warnings = validate_program(program)
        errors.extend(f"{path.name}: {error}" for error in graph_errors)
        warnings.extend(f"{path.name}: {warning}" for warning in graph_warnings)
        errors.extend(check_generator(program, playlists_by_name[name], rules))

    # Manifest consistency.
    manifest_pool_names = {entry.get("program_name") for entry in manifest.get("pools", [])}
    if manifest_pool_names != seen_pools:
        errors.append("manifest pool list does not match generated pool files")
    manifest_generator_names = {entry.get("playlist_name") for entry in manifest.get("generators", [])}
    if manifest_generator_names != seen_generators:
        errors.append("manifest generator list does not match generated generator files")

    summary = {
        "manifest_mode": manifest.get("mode"),
        "pool_files": len(pool_files),
        "generator_files": len(generator_files),
        "pool_names": len(seen_pools),
        "generator_names": len(seen_generators),
        "errors": len(errors),
        "warnings": len(warnings),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print("\nPrograms OK.")


if __name__ == "__main__":
    main()
