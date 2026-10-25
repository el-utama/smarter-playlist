#!/usr/bin/env python3
"""Build config files for the 120-playlist SmarterPlaylists project.

Inputs:
  config/taxonomy.draft.json
  config/rules.json
  exports/release_manifest.json
  exports/tracks_all.csv

Outputs:
  config/priority_artists.json
  config/series_exclusion_uris.txt
  config/priority_tracks.csv
  config/priority_summary.json
  config/pool_manifest.json
  config/pool_uris.json
  config/playlists_120.draft.json

This script does not call Spotify or SmarterPlaylists.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
EXPORTS_DIR = ROOT / "exports"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: str | int | None, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_bool(value: str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def round_float(value: float) -> float:
    return round(value, 4)


def apply_modifier(
    base_range: list[float] | tuple[float, float],
    modifier: float,
    *,
    low: float,
    high: float,
    integer: bool = False,
) -> list[float] | list[int]:
    adjusted = [clamp(float(base_range[0]) + modifier, low, high), clamp(float(base_range[1]) + modifier, low, high)]
    if integer:
        return [int(round(adjusted[0])), int(round(adjusted[1]))]
    return [round_float(adjusted[0]), round_float(adjusted[1])]


def build_playlist_description(category_label: str, genre: str, mood: str) -> str:
    """Build a concise, professional English description for Spotify (max 300 chars)."""
    intros = {
        "Morning": "Start your morning with",
        "Midday": "Power through midday with",
        "Afternoon": "Soundtrack your afternoon with",
        "Night": "Unwind into the night with",
    }
    intro = intros.get(category_label, "Enjoy")
    phrase = f"{mood.lower()} {genre.lower()}"
    # Avoid awkward repetition such as "dreamy dream pop" or "groovy funk & groove".
    if genre == "Dream Pop & Shoegaze" and mood == "Dreamy":
        phrase = "hazy dream pop & shoegaze"
    elif genre == "Funk & Groove" and mood == "Groovy":
        phrase = "feel-good funk & groove"
    article = "an" if phrase[:1] in "aeiou" else "a"
    return (
        f"{intro} {article} {phrase} mix. "
        "Artist-first picks and new discoveries, sequenced for a smooth flow. "
        "Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}."
    )


def date_key(value: str) -> tuple[int, int, int]:
    """Return a comparable (year, month, day) tuple for a Spotify date string."""
    if not value:
        return (0, 0, 0)
    parts = re.split(r"[-/]", str(value).strip())
    year = as_int(parts[0]) if parts else 0
    month = as_int(parts[1]) if len(parts) > 1 else 0
    day = as_int(parts[2]) if len(parts) > 2 else 0
    return (year, month, day)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def build() -> None:
    taxonomy = load_json(CONFIG_DIR / "taxonomy.draft.json")
    rules = load_json(CONFIG_DIR / "rules.json")
    release_manifest = load_json(EXPORTS_DIR / "release_manifest.json")
    tracks = load_csv(EXPORTS_DIR / "tracks_all.csv")

    # ------------------------------------------------------------------
    # Priority artists (25 No Detours) + eL Utama
    # ------------------------------------------------------------------
    priority_artists: list[dict[str, Any]] = []
    for artist in release_manifest:
        priority_artists.append(
            {
                "name": artist.get("name", ""),
                "uri": artist.get("uri", ""),
                "track_count": as_int(artist.get("total")),
            }
        )

    priority_artist_names = [artist["name"] for artist in priority_artists] + ["eL Utama"]
    priority_artist_names = [name for name in priority_artist_names if name]
    priority_artist_names_text = ", ".join(priority_artist_names)

    priority_artists_doc = {
        "_note": "25 No Detours artists dari exports/release_manifest.json + eL Utama sebagai sumber playlist.",
        "version": 1,
        "artists": priority_artists,
        "el_utama": {
            "name": "eL Utama",
            "playlist_uri": rules["el_utama_playlist_uri"],
        },
        "all_names": priority_artist_names,
        "all_names_text": priority_artist_names_text,
        "artist_uris_text": " ".join(artist["uri"] for artist in priority_artists),
    }
    (CONFIG_DIR / "priority_artists.json").write_text(
        json.dumps(priority_artists_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Series exclusion URIs (16 existing series playlists)
    # ------------------------------------------------------------------
    series_tracks: list[dict[str, str]] = []
    seen_series_uris: set[str] = set()
    for track in tracks:
        if track.get("kind") != "series":
            continue
        uri = track.get("track_uri", "").strip()
        if not uri or uri in seen_series_uris:
            continue
        seen_series_uris.add(uri)
        series_tracks.append(track)

    series_uris = [track["track_uri"].strip() for track in series_tracks]
    (CONFIG_DIR / "series_exclusion_uris.txt").write_text(
        "\n".join(series_uris) + ("\n" if series_uris else ""),
        encoding="utf-8",
    )

    series_uri_set = set(series_uris)
    series_name_artist_set: set[tuple[str, str]] = set()
    for track in series_tracks:
        title = (track.get("track_name") or "").strip().lower()
        artists = (track.get("artists") or track.get("artist") or "").strip().lower()
        if title and artists:
            series_name_artist_set.add((title, artists))

    # ------------------------------------------------------------------
    # Priority tracks: filter, dedup, sort
    # ------------------------------------------------------------------
    exclude_regex_text = str(rules.get("exclude_patterns_regex") or "")
    exclude_regex = re.compile(exclude_regex_text) if exclude_regex_text else None
    min_duration = as_int(rules.get("min_duration_ms"), 0)
    max_duration = as_int(rules.get("max_duration_ms"), 0)
    exclude_short = bool(rules.get("exclude_short_tracks", False))
    exclude_patterns = bool(rules.get("exclude_patterns", False))
    exclude_series = bool(rules.get("exclude_series_tracks", False))
    priority_exclude_series = bool(rules.get("priority_exclude_series_tracks", False))

    priority_raw: list[dict[str, Any]] = []
    seen_priority_uris: set[str] = set()
    for track in tracks:
        if track.get("kind") not in {"artist", "el"}:
            continue
        uri = (track.get("track_uri") or "").strip()
        if not uri or uri in seen_priority_uris:
            continue
        seen_priority_uris.add(uri)
        priority_raw.append(
            {
                "artist": (track.get("artist") or "").strip(),
                "track_name": (track.get("track_name") or "").strip(),
                "track_uri": uri,
                "popularity": as_int(track.get("popularity")),
                "release_date": (track.get("release_date") or "").strip(),
                "duration_ms": as_int(track.get("duration_ms")),
                "explicit": as_bool(track.get("explicit")),
                "kind": (track.get("kind") or "").strip(),
            }
        )

    priority_filtered: list[dict[str, Any]] = []
    removed_duration = 0
    removed_pattern = 0
    removed_series = 0
    for track in priority_raw:
        duration = track["duration_ms"]
        if exclude_short and ((min_duration and duration < min_duration) or (max_duration and duration > max_duration)):
            removed_duration += 1
            continue
        if exclude_patterns and exclude_regex and exclude_regex.search(track["track_name"]):
            removed_pattern += 1
            continue
        if exclude_series and priority_exclude_series:
            title = track["track_name"].lower()
            artists = track["artist"].lower()
            if track["track_uri"] in series_uri_set or (title, artists) in series_name_artist_set:
                removed_series += 1
                continue
        priority_filtered.append(track)

    priority_filtered.sort(
        key=lambda item: (
            item["popularity"],
            tuple(-part for part in date_key(item["release_date"])),
            item["artist"].lower(),
            item["track_name"].lower(),
        )
    )

    with (CONFIG_DIR / "priority_tracks.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["artist", "track_name", "track_uri", "popularity", "release_date", "duration_ms", "explicit"],
        )
        writer.writeheader()
        for track in priority_filtered:
            writer.writerow(
                {
                    "artist": track["artist"],
                    "track_name": track["track_name"],
                    "track_uri": track["track_uri"],
                    "popularity": track["popularity"],
                    "release_date": track["release_date"],
                    "duration_ms": track["duration_ms"],
                    "explicit": str(track["explicit"]).lower(),
                }
            )

    priority_pool_size = len(priority_filtered)
    if priority_pool_size <= 0:
        raise SystemExit("Priority pool is empty after filters. Check config/rules.json.")

    priority_summary = {
        "raw_unique_tracks": len(priority_raw),
        "after_duration_filter": len(priority_raw) - removed_duration,
        "after_pattern_filter": len(priority_raw) - removed_duration - removed_pattern,
        "after_series_exclusion": priority_pool_size,
        "removed_by_duration": removed_duration,
        "removed_by_pattern": removed_pattern,
        "removed_by_series_exclusion": removed_series,
        "priority_pool_size": priority_pool_size,
        "series_exclusion_uri_count": len(series_uris),
        "priority_artist_count": len(priority_artist_names),
        "filters": {
            "exclude_short_tracks": exclude_short,
            "min_duration_ms": min_duration,
            "max_duration_ms": max_duration,
            "exclude_patterns": exclude_patterns,
            "exclude_patterns_regex": exclude_regex_text,
            "exclude_series_tracks": exclude_series,
            "priority_exclude_series_tracks": priority_exclude_series,
        },
    }
    (CONFIG_DIR / "priority_summary.json").write_text(
        json.dumps(priority_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Pools (1 priority pool + 20 genre pools)
    # ------------------------------------------------------------------
    categories: dict[str, Any] = taxonomy["categories"]
    category_keys = list(categories.keys())

    pools: list[dict[str, Any]] = []
    pools.append(
        {
            "type": "priority",
            "program_name": rules["priority_pool_program_name"],
            "category": "",
            "category_label": "Priority",
            "genre": "",
            "genre_filter": "",
            "tags": [],
            "descriptions": [],
            "radio_seeds": [],
            "explicit_mode": "allow",
            "pool_size": priority_pool_size,
            "min_duration_ms": min_duration,
            "max_duration_ms": max_duration,
            "exclude_patterns_regex": exclude_regex_text,
            "exclude_series_tracks": priority_exclude_series,
            "priority_artist_uris_text": priority_artists_doc["artist_uris_text"],
            "priority_track_uris_text": "\n".join(track["track_uri"] for track in priority_filtered),
            "el_utama_playlist_uri": rules["el_utama_playlist_uri"],
            "pool_playlist_uri": rules["priority_pool_playlist_uri"],
            "comment": (
                f"POOL: {rules['priority_pool_program_name']}\n"
                f"Contents: {priority_pool_size} priority tracks from the 26 artists, sourced from config/priority_tracks.csv.\n"
                "Rebuild this program when the priority catalog changes.\n"
                "Internal pool; no need to follow.\n"
                "Do not change the Sorter order: release_date descending, then popularity ascending."
            ),
        }
    )

    for category_index, category_key in enumerate(category_keys):
        category = categories[category_key]
        base_ranges = category["base_ranges"]
        explicit_mode = rules.get("explicit_modes", {}).get(category_key, category.get("explicit_mode", "allow"))
        for genre_index, genre in enumerate(category["genres"]):
            program_name = rules["pool_name_template"].format(
                prefix=category["prefix"],
                genre=genre["name"],
            )
            seed_offset = (category_index * 5 + genre_index) % max(len(priority_artists), 1)
            radio_seeds = []
            for seed_index in range(as_int(rules.get("radio_seed_count"), 3)):
                artist = priority_artists[(seed_offset + seed_index) % len(priority_artists)]
                radio_seeds.append({"name": artist["name"], "uri": artist["uri"]})
            pool = {
                "type": "genre",
                "program_name": program_name,
                "category": category_key,
                "category_label": category["label"],
                "genre": genre["name"],
                "genre_filter": genre.get("filter", ""),
                "artist_genre": genre.get("artist_genre") or genre.get("filter", ""),
                "tags": genre.get("tags", []),
                "descriptions": genre.get("descriptions", []),
                "radio_seeds": radio_seeds,
                "explicit_mode": explicit_mode,
                "pool_size": as_int(rules.get("pool_size"), 3000),
                "tag_limit": as_int(rules.get("tag_limit"), 1000),
                "description_limit": as_int(rules.get("description_limit"), 200),
                "genre_artists_count": as_int(rules.get("genre_artists_count"), 50),
                "genre_tracks_per_artist": as_int(rules.get("genre_tracks_per_artist"), 10),
                "base_ranges": base_ranges,
                "priority_artist_names_text": priority_artist_names_text,
                "pool_playlist_uri": rules.get("pool_playlist_uri_placeholder", "spotify:playlist:REPLACE_ME"),
                "comment": (
                    f"POOL: {program_name}\n"
                    f"Category: {category['label']} · Genre: {genre['name']}\n"
                    f"Tags: {', '.join(genre.get('tags', []))}\n"
                    f"Genre filter: {genre.get('filter') or '(none)'}\n"
                    f"Explicit: {explicit_mode}\n"
                    "Internal pool; no need to follow."
                ),
            }
            pools.append(pool)

    # Pool URIs are the one thing that must survive a config regeneration.
    # Seed config/pool_uris.json with placeholders, then preserve user edits.
    pool_uris_path = CONFIG_DIR / "pool_uris.json"
    existing_pool_uris: dict[str, str] = {}
    if pool_uris_path.exists():
        existing_pool_uris = load_json(pool_uris_path)
        if not isinstance(existing_pool_uris, dict):
            raise SystemExit("config/pool_uris.json must contain a JSON object")
    updated_pool_uris: dict[str, str] = {}
    for pool in pools:
        program_name = pool["program_name"]
        default_uri = pool.get("pool_playlist_uri") or rules.get(
            "pool_playlist_uri_placeholder", "spotify:playlist:REPLACE_ME"
        )
        uri = existing_pool_uris.get(program_name, default_uri)
        updated_pool_uris[program_name] = uri
        pool["pool_playlist_uri"] = uri
    pool_uris_path.write_text(
        json.dumps(updated_pool_uris, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    pool_manifest = {
        "_note": "21 pool internal: 1 priority + 20 genre (4 kategori x 5 genre).",
        "version": 1,
        "pools": pools,
    }
    (CONFIG_DIR / "pool_manifest.json").write_text(
        json.dumps(pool_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # 120 playlist entries
    # ------------------------------------------------------------------
    priority_slice = as_int(rules.get("priority_slice"), 200)
    global_slice = as_int(rules.get("global_slice"), 300)
    priority_share = as_int(rules.get("priority_share"), 60)
    global_share = as_int(rules.get("global_share"), 40)
    global_pool_size_estimate = as_int(rules.get("global_pool_size_estimate"), 3000)
    priority_max_per_artist = as_int(rules.get("priority_max_per_artist"), 8)
    global_max_per_artist = as_int(rules.get("global_max_per_artist"), 3)
    mos_limit = as_int(rules.get("mos_limit"), 120)
    cap_seconds = as_int(rules.get("cap_seconds"), 21600)
    el_utama_weight = str(rules.get("el_utama_weight", "high"))
    genre_match_weight = str(rules.get("genre_match_weight", "medium"))

    pool_by_program = {pool["program_name"]: pool for pool in pools}

    playlists: list[dict[str, Any]] = []
    for category_key in category_keys:
        category = categories[category_key]
        explicit_mode = rules.get("explicit_modes", {}).get(category_key, category.get("explicit_mode", "allow"))
        index = 0
        for genre in category["genres"]:
            for mood in category["moods"]:
                index += 1
                name = rules["playlist_name_template"].format(
                    prefix=category["prefix"],
                    index=index,
                    genre=genre["name"],
                    mood=mood["name"],
                )
                pool_program_name = rules["pool_name_template"].format(
                    prefix=category["prefix"],
                    genre=genre["name"],
                )
                pool = pool_by_program[pool_program_name]
                base_ranges = category["base_ranges"]
                modifiers = mood.get("modifiers", {})

                energy_range = apply_modifier(base_ranges["energy"], float(modifiers.get("energy", 0.0)), low=0.0, high=1.0)
                valence_range = apply_modifier(base_ranges["valence"], float(modifiers.get("valence", 0.0)), low=0.0, high=1.0)
                tempo_range = apply_modifier(
                    base_ranges["tempo"],
                    float(modifiers.get("tempo", 0.0)),
                    low=40.0,
                    high=200.0,
                    integer=True,
                )
                danceability_range = apply_modifier(
                    base_ranges["danceability"],
                    float(modifiers.get("danceability", 0.0)),
                    low=0.0,
                    high=1.0,
                )
                acousticness_range = apply_modifier(
                    base_ranges["acousticness"],
                    float(modifiers.get("acousticness", 0.0)),
                    low=0.0,
                    high=1.0,
                )

                priority_offset = ((index - 1) * priority_slice) % priority_pool_size
                global_offset = ((index - 1) * global_slice) % max(global_pool_size_estimate, 1)
                genre_filter = str(genre.get("filter", "") or "")
                artist_genre = str(genre.get("artist_genre") or genre_filter)
                genre_match_value = genre_filter or artist_genre
                genre_weight = genre_match_weight if genre_match_value else "off"

                playlist = {
                    "name": name,
                    "description": build_playlist_description(category["label"], genre["name"], mood["name"]),
                    "slug": slugify(name),
                    "category": category_key,
                    "category_label": category["label"],
                    "index": index,
                    "genre": genre["name"],
                    "mood": mood["name"],
                    "pool_program_name": pool_program_name,
                    "pool_playlist_uri": pool["pool_playlist_uri"],
                    "priority_pool_program_name": rules["priority_pool_program_name"],
                    "priority_pool_playlist_uri": pool_by_program[rules["priority_pool_program_name"]]["pool_playlist_uri"],
                    "priority_offset": priority_offset,
                    "global_offset": global_offset,
                    "priority_slice": priority_slice,
                    "global_slice": global_slice,
                    "priority_max_per_artist": priority_max_per_artist,
                    "global_max_per_artist": global_max_per_artist,
                    "priority_share": priority_share,
                    "global_share": global_share,
                    "priority_pool_size": priority_pool_size,
                    "global_pool_size_estimate": global_pool_size_estimate,
                    "energy_range": energy_range,
                    "valence_range": valence_range,
                    "tempo_range": tempo_range,
                    "danceability_range": danceability_range,
                    "acousticness_range": acousticness_range,
                    "genre_filter": genre_filter,
                    "artist_genre": artist_genre,
                    "genre_match_value": genre_match_value,
                    "genre_match_weight": genre_weight,
                    "genre_tags": genre.get("tags", []),
                    "genre_descriptions": genre.get("descriptions", []),
                    "explicit_mode": explicit_mode,
                    "explicit_filter_value": False if explicit_mode == "clean" else None,
                    "el_utama_weight": el_utama_weight,
                    "mos_limit": mos_limit,
                    "cap_seconds": cap_seconds,
                    "comment": (
                        f"PLAYLIST: {name}\n"
                        f"Category: {category['label']} · Genre: {genre['name']} · Mood: {mood['name']}\n"
                        f"Priority offset: {priority_offset} · Global offset: {global_offset}\n"
                        f"Priority share: {priority_share}% · Global: {global_share}%\n"
                        "Do not change ShorterThan (6 hours) or match-max-run (no consecutive artist)."
                    ),
                }
                playlists.append(playlist)

    if len(playlists) != 120:
        raise SystemExit(f"Expected 120 playlists, got {len(playlists)}")

    playlists_doc = {
        "_note": "APPROVED config 120 playlist (2026-10-24). English titles and descriptions. Edit taxonomy.draft.json lalu regenerate.",
        "version": 1,
        "rules": rules,
        "categories": {
            key: {
                "label": value["label"],
                "prefix": value["prefix"],
                "explicit_mode": rules.get("explicit_modes", {}).get(key, value.get("explicit_mode", "allow")),
                "base_ranges": value["base_ranges"],
                "genres": value["genres"],
                "moods": value["moods"],
            }
            for key, value in categories.items()
        },
        "pools": pools,
        "playlists": playlists,
    }
    (CONFIG_DIR / "playlists_120.draft.json").write_text(
        json.dumps(playlists_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    summary = {
        "priority_artists": len(priority_artists),
        "priority_artist_names": len(priority_artist_names),
        "priority_raw_tracks": len(priority_raw),
        "priority_pool_size": priority_pool_size,
        "series_exclusion_uris": len(series_uris),
        "pools": len(pools),
        "genre_pools": len(pools) - 1,
        "pool_uris_total": len(updated_pool_uris),
        "pool_uris_filled": sum(1 for uri in updated_pool_uris.values() if "REPLACE_ME" not in uri),
        "playlists": len(playlists),
        "categories": {key: len([p for p in playlists if p["category"] == key]) for key in category_keys},
        "priority_share": priority_share,
        "global_share": global_share,
        "cap_seconds": cap_seconds,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
