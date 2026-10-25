#!/usr/bin/env python3
"""Validate the local 120-playlist configuration.

This script does not call Spotify or SmarterPlaylists.

Usage:
  python tools/validate_config.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def date_key(value: str) -> tuple[int, int, int]:
    if not value:
        return (0, 0, 0)
    parts = re.split(r"[-/]", str(value).strip())
    year = as_int(parts[0]) if parts else 0
    month = as_int(parts[1]) if len(parts) > 1 else 0
    day = as_int(parts[2]) if len(parts) > 2 else 0
    return (year, month, day)


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    taxonomy = load_json(CONFIG_DIR / "taxonomy.draft.json")
    rules = load_json(CONFIG_DIR / "rules.json")
    priority_artists = load_json(CONFIG_DIR / "priority_artists.json")
    priority_summary = load_json(CONFIG_DIR / "priority_summary.json")
    pool_manifest = load_json(CONFIG_DIR / "pool_manifest.json")
    pool_uris = load_json(CONFIG_DIR / "pool_uris.json")
    playlists_doc = load_json(CONFIG_DIR / "playlists_120.draft.json")

    # ------------------------------------------------------------------
    # Taxonomy
    # ------------------------------------------------------------------
    categories = taxonomy.get("categories", {})
    expected_categories = ["pagi", "siang", "sore", "malam"]
    if list(categories.keys()) != expected_categories:
        errors.append(f"taxonomy categories should be {expected_categories}, got {list(categories.keys())}")

    for category_key, category in categories.items():
        genres = category.get("genres", [])
        moods = category.get("moods", [])
        if len(genres) != 5:
            errors.append(f"{category_key}: expected 5 genres, got {len(genres)}")
        if len(moods) != 6:
            errors.append(f"{category_key}: expected 6 moods, got {len(moods)}")
        genre_names = [genre.get("name", "") for genre in genres]
        mood_names = [mood.get("name", "") for mood in moods]
        if len(set(genre_names)) != len(genre_names):
            errors.append(f"{category_key}: duplicate genre names")
        if len(set(mood_names)) != len(mood_names):
            errors.append(f"{category_key}: duplicate mood names")
        for genre in genres:
            name = genre.get("name", "")
            if not name:
                errors.append(f"{category_key}: genre without name")
            if len(genre.get("tags", [])) != 3:
                errors.append(f"{category_key}/{name}: expected 3 tags")
            if len(genre.get("descriptions", [])) != 2:
                errors.append(f"{category_key}/{name}: expected 2 descriptions")
            if not genre.get("filter") and not genre.get("artist_genre"):
                errors.append(f"{category_key}/{name}: needs filter or artist_genre")
        for mood in moods:
            if not mood.get("name"):
                errors.append(f"{category_key}: mood without name")
            if not isinstance(mood.get("modifiers"), dict):
                errors.append(f"{category_key}/{mood.get('name')}: missing modifiers")
        base = category.get("base_ranges", {})
        for attr in ["energy", "valence", "tempo", "danceability", "acousticness"]:
            if attr not in base or not isinstance(base[attr], list) or len(base[attr]) != 2:
                errors.append(f"{category_key}: base_ranges.{attr} must be a two-item list")

    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------
    if as_int(rules.get("priority_share")) + as_int(rules.get("global_share")) != 100:
        errors.append("priority_share + global_share must equal 100")
    if as_int(rules.get("cap_seconds")) != 21600:
        errors.append("cap_seconds must be 21600 (6 hours)")
    if as_int(rules.get("priority_slice")) <= 0 or as_int(rules.get("global_slice")) <= 0:
        errors.append("slices must be positive")
    if as_int(rules.get("priority_max_per_artist")) <= 0 or as_int(rules.get("global_max_per_artist")) <= 0:
        errors.append("max per artist must be positive")
    if as_int(rules.get("min_duration_ms")) >= as_int(rules.get("max_duration_ms")):
        errors.append("min_duration_ms must be less than max_duration_ms")
    try:
        re.compile(str(rules.get("exclude_patterns_regex", "")))
    except re.error as exc:
        errors.append(f"exclude_patterns_regex is invalid: {exc}")
    for category_key in expected_categories:
        mode = rules.get("explicit_modes", {}).get(category_key)
        if mode not in {"clean", "allow"}:
            errors.append(f"explicit_modes.{category_key} must be 'clean' or 'allow'")
    if rules.get("priority_exclude_series_tracks") is not False:
        warnings.append("priority_exclude_series_tracks is not false; priority pool may shrink")

    # ------------------------------------------------------------------
    # Priority artists
    # ------------------------------------------------------------------
    artists = priority_artists.get("artists", [])
    if len(artists) != 25:
        errors.append(f"expected 25 No Detours artists, got {len(artists)}")
    for artist in artists:
        if not artist.get("name"):
            errors.append("priority artist without name")
        if not str(artist.get("uri", "")).startswith("spotify:artist:"):
            errors.append(f"priority artist {artist.get('name')!r} has invalid URI")
    if len(set(artist.get("uri") for artist in artists)) != len(artists):
        errors.append("duplicate priority artist URIs")
    all_names = priority_artists.get("all_names", [])
    if len(all_names) != 26:
        errors.append(f"expected 26 priority artist names, got {len(all_names)}")
    if "eL Utama" not in all_names:
        errors.append("eL Utama missing from all_names")
    if not str(priority_artists.get("el_utama", {}).get("playlist_uri", "")).startswith("spotify:playlist:"):
        errors.append("eL Utama playlist URI is invalid")

    # ------------------------------------------------------------------
    # Priority tracks CSV and summary
    # ------------------------------------------------------------------
    with (CONFIG_DIR / "priority_tracks.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_columns = ["artist", "track_name", "track_uri", "popularity", "release_date", "duration_ms", "explicit"]
    if rows and list(rows[0].keys()) != expected_columns:
        errors.append(f"priority_tracks.csv columns should be {expected_columns}")
    if len(rows) != as_int(priority_summary.get("priority_pool_size")):
        errors.append(
            f"priority_tracks.csv has {len(rows)} rows but priority_summary says "
            f"{priority_summary.get('priority_pool_size')}"
        )
    if len({row.get("track_uri") for row in rows}) != len(rows):
        errors.append("priority_tracks.csv contains duplicate track URIs")
    previous_key: tuple[Any, ...] | None = None
    for row in rows:
        key = (
            as_int(row.get("popularity")),
            tuple(-part for part in date_key(row.get("release_date", ""))),
            str(row.get("artist", "")).lower(),
            str(row.get("track_name", "")).lower(),
        )
        if previous_key is not None and key < previous_key:
            errors.append("priority_tracks.csv is not sorted by popularity asc, then release_date desc")
            break
        previous_key = key
    for row in rows:
        if not str(row.get("track_uri", "")).startswith("spotify:track:"):
            errors.append(f"invalid priority track URI: {row.get('track_uri')!r}")
            break

    # ------------------------------------------------------------------
    # Series exclusion
    # ------------------------------------------------------------------
    series_uris = [
        line.strip()
        for line in (CONFIG_DIR / "series_exclusion_uris.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(series_uris) != len(set(series_uris)):
        errors.append("series_exclusion_uris.txt contains duplicates")
    if len(series_uris) != as_int(priority_summary.get("series_exclusion_uri_count")):
        errors.append(
            f"series_exclusion_uris.txt has {len(series_uris)} URIs but priority_summary says "
            f"{priority_summary.get('series_exclusion_uri_count')}"
        )
    for uri in series_uris:
        if not uri.startswith("spotify:track:"):
            errors.append(f"invalid series exclusion URI: {uri!r}")
            break

    # ------------------------------------------------------------------
    # Pools
    # ------------------------------------------------------------------
    pools = pool_manifest.get("pools", [])
    if len(pools) != 21:
        errors.append(f"expected 21 pools, got {len(pools)}")
    priority_pools = [pool for pool in pools if pool.get("type") == "priority"]
    genre_pools = [pool for pool in pools if pool.get("type") == "genre"]
    if len(priority_pools) != 1:
        errors.append(f"expected 1 priority pool, got {len(priority_pools)}")
    if len(genre_pools) != 20:
        errors.append(f"expected 20 genre pools, got {len(genre_pools)}")
    if len({pool.get("program_name") for pool in pools}) != len(pools):
        errors.append("duplicate pool program names")

    if len(pool_uris) != len(pools):
        errors.append(f"pool_uris.json should have {len(pools)} entries, got {len(pool_uris)}")
    for pool in pools:
        program_name = pool.get("program_name", "")
        if program_name not in pool_uris:
            errors.append(f"pool_uris.json missing {program_name!r}")
            continue
        uri = str(pool_uris[program_name])
        if "REPLACE_ME" not in uri and not uri.startswith("spotify:playlist:"):
            errors.append(f"pool_uris.json has invalid URI for {program_name!r}")
        if pool.get("pool_playlist_uri") != uri:
            errors.append(f"pool_manifest URI for {program_name!r} does not match pool_uris.json")

    priority_pool = priority_pools[0] if priority_pools else {}
    if priority_pool:
        if len(str(priority_pool.get("priority_artist_uris_text", "")).split()) != 25:
            errors.append("priority pool does not have exactly 25 artist URIs")
        if not str(priority_pool.get("el_utama_playlist_uri", "")).startswith("spotify:playlist:"):
            errors.append("priority pool has invalid eL Utama playlist URI")
        if priority_pool.get("exclude_series_tracks") is not False:
            errors.append("priority pool must not exclude series tracks")

    for pool in genre_pools:
        name = pool.get("program_name", "")
        if len(pool.get("tags", [])) != 3:
            errors.append(f"{name}: expected 3 tags")
        if len(pool.get("descriptions", [])) != 2:
            errors.append(f"{name}: expected 2 descriptions")
        if len(pool.get("radio_seeds", [])) != 3:
            errors.append(f"{name}: expected 3 radio seeds")
        if len(str(pool.get("priority_artist_names_text", "")).split(",")) != 26:
            errors.append(f"{name}: expected 26 priority artist names")
        if not pool.get("artist_genre"):
            errors.append(f"{name}: missing artist_genre")
        if as_int(pool.get("pool_size")) <= 0:
            errors.append(f"{name}: pool_size must be positive")
        base = pool.get("base_ranges", {})
        for attr in ["energy", "valence", "tempo", "danceability", "acousticness"]:
            if attr not in base or len(base[attr]) != 2:
                errors.append(f"{name}: missing base_ranges.{attr}")

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------
    playlists = playlists_doc.get("playlists", [])
    if len(playlists) != 120:
        errors.append(f"expected 120 playlists, got {len(playlists)}")
    if playlists_doc.get("pools") != pools:
        errors.append("playlists_120.draft.json pools differ from pool_manifest.json")
    if len({playlist.get("name") for playlist in playlists}) != len(playlists):
        errors.append("duplicate playlist names")
    if len({playlist.get("slug") for playlist in playlists}) != len(playlists):
        errors.append("duplicate playlist slugs")

    pool_by_name = {pool.get("program_name"): pool for pool in pools}
    per_category: dict[str, int] = {}
    for playlist in playlists:
        name = playlist.get("name", "")
        category = playlist.get("category", "")
        per_category[category] = per_category.get(category, 0) + 1
        for field in [
            "name", "description", "slug", "category", "category_label", "index", "genre", "mood",
            "pool_program_name", "priority_pool_program_name", "priority_pool_playlist_uri",
            "pool_playlist_uri", "priority_offset", "global_offset", "priority_slice",
            "global_slice", "priority_max_per_artist", "global_max_per_artist",
            "priority_share", "global_share", "priority_pool_size", "energy_range",
            "valence_range", "tempo_range", "danceability_range", "acousticness_range",
            "genre_filter", "artist_genre", "genre_match_value", "genre_match_weight",
            "explicit_mode", "el_utama_weight", "mos_limit", "cap_seconds", "comment",
        ]:
            if field not in playlist:
                errors.append(f"{name}: missing field {field}")
        description = str(playlist.get("description", ""))
        if not description:
            errors.append(f"{name}: empty description")
        elif len(description) > 300:
            errors.append(f"{name}: description is {len(description)} chars (Spotify max 300)")
        if "${NUM_TRACKS}" not in description or "${DURATION}" not in description:
            warnings.append(f"{name}: description does not use ${NUM_TRACKS} and ${DURATION}")
        if playlist.get("pool_program_name") not in pool_by_name:
            errors.append(f"{name}: unknown pool {playlist.get('pool_program_name')!r}")
        if playlist.get("priority_pool_program_name") != rules.get("priority_pool_program_name"):
            errors.append(f"{name}: wrong priority pool program name")
        if priority_pool and playlist.get("priority_pool_playlist_uri") != priority_pool.get("pool_playlist_uri"):
            errors.append(f"{name}: priority pool URI does not match the priority pool entry")
        if as_int(playlist.get("priority_share")) + as_int(playlist.get("global_share")) != 100:
            errors.append(f"{name}: shares do not total 100")
        if as_int(playlist.get("cap_seconds")) != 21600:
            errors.append(f"{name}: cap_seconds is not 21600")
        if playlist.get("explicit_mode") not in {"clean", "allow"}:
            errors.append(f"{name}: invalid explicit_mode")
        if playlist.get("explicit_mode") == "clean" and playlist.get("explicit_filter_value") is not False:
            errors.append(f"{name}: clean playlist must set explicit_filter_value false")
        if playlist.get("explicit_mode") == "allow" and playlist.get("explicit_filter_value") is not None:
            errors.append(f"{name}: allow playlist must set explicit_filter_value null")
        if as_int(playlist.get("priority_offset")) >= max(as_int(playlist.get("priority_pool_size")), 1):
            errors.append(f"{name}: priority_offset is outside the priority pool")
        if as_int(playlist.get("global_offset")) >= max(as_int(playlist.get("global_pool_size_estimate")), 1):
            errors.append(f"{name}: global_offset is outside the global pool estimate")
        if not playlist.get("genre_match_value"):
            errors.append(f"{name}: genre_match_value is empty")
        for attr in ["energy_range", "valence_range", "danceability_range", "acousticness_range"]:
            values = playlist.get(attr, [])
            if len(values) != 2 or not (0.0 <= float(values[0]) <= float(values[1]) <= 1.0):
                errors.append(f"{name}: {attr} must be a valid 0..1 range")
        tempo = playlist.get("tempo_range", [])
        if len(tempo) != 2 or not (40 <= float(tempo[0]) <= float(tempo[1]) <= 200):
            errors.append(f"{name}: tempo_range must be within 40..200")

    for category_key in expected_categories:
        if per_category.get(category_key) != 30:
            errors.append(f"{category_key}: expected 30 playlists, got {per_category.get(category_key, 0)}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    summary = {
        "categories": len(categories),
        "genres": sum(len(category.get("genres", [])) for category in categories.values()),
        "moods": sum(len(category.get("moods", [])) for category in categories.values()),
        "priority_artists": len(artists),
        "priority_artist_names": len(all_names),
        "priority_tracks": len(rows),
        "series_exclusion_uris": len(series_uris),
        "pools": len(pools),
        "genre_pools": len(genre_pools),
        "pool_uris_filled": sum(1 for uri in pool_uris.values() if "REPLACE_ME" not in str(uri)),
        "playlists": len(playlists),
        "per_category": per_category,
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
    print("\nConfig OK.")


if __name__ == "__main__":
    main()
