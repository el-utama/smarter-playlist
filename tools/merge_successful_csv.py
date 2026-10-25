#!/usr/bin/env python3
"""Merge hasil run ke config/successful_playlists.csv.

Menggabungkan:
  1. Baris lama dari successful_playlists.csv (dipertahankan durasi aslinya)
  2. Program baru dari /api/programs/enriched yang punya run sukses
     (playlist_uri dari API, deskripsi dari config, durasi diestimasi)

Output ditimpa ke config/successful_playlists.csv.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
SUCCESS_CSV = CONFIG_DIR / "successful_playlists.csv"
PLAYLISTS_DRAFT = CONFIG_DIR / "playlists_120.draft.json"
POOL_MANIFEST = CONFIG_DIR / "pool_manifest.json"

sys.path.insert(0, str(ROOT / "tools"))
from sm_session import SmarterPlaylistsSession  # noqa: E402


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def build_description_map() -> dict[str, str]:
    """Map nama program -> deskripsi dari config."""
    desc: dict[str, str] = {}

    # Playlist generator descriptions
    draft = load_json(PLAYLISTS_DRAFT)
    for p in draft.get("playlists", []):
        desc[p["name"]] = p.get("description", "")
    for pool in draft.get("pools", []):
        name = pool.get("program_name", "")
        if name:
            desc[name] = pool.get("comment", "")

    # Pool manifest descriptions (fallback)
    manifest = load_json(POOL_MANIFEST)
    for pool in manifest.get("pools", []):
        name = pool.get("program_name", "")
        if name and name not in desc:
            desc[name] = pool.get("comment", "")

    return desc


def estimate_duration(tracks: int, is_pool: bool) -> str:
    """Estimasi durasi playlist dari jumlah track."""
    if tracks <= 0:
        return "?"
    # Playlist generator: ~3.5 menit per track, cap 6 jam
    # Pool: semua track, ~4 menit per track
    mins_per_track = 4.0 if is_pool else 3.5
    total_minutes = tracks * mins_per_track
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def main() -> None:
    sm = SmarterPlaylistsSession()
    sess = sm.load()

    # 1. Ambil semua program dari enriched API
    r = sm.get("/api/programs/enriched")
    if not r.ok:
        print(f"Gagal ambil enriched API: HTTP {r.status_code}")
        sys.exit(1)
    programs: list[dict[str, Any]] = r.json()

    # 2. Bangun deskripsi dari config
    desc_map = build_description_map()

    # 3. Baca existing successful_playlists.csv
    existing_rows: list[dict[str, str]] = []
    existing_names: set[str] = set()
    if SUCCESS_CSV.exists():
        with SUCCESS_CSV.open("r", encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                existing_rows.append(row)
                existing_names.add((row.get("Program Name") or "").strip())

    # 4. Bangun baris baru dari enriched API (hanya yang run sukses)
    now = datetime.now(timezone.utc).astimezone()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    new_rows: list[dict[str, str]] = []
    for prog in programs:
        name = (prog.get("name") or "").strip()
        if not name:
            continue
        if name in existing_names:
            continue  # Sudah ada, pertahankan baris lama

        playlist_uri = prog.get("playlist_uri") or ""
        run_stats = prog.get("run_stats") or {}
        last_run_status = run_stats.get("last_run_status", "")
        last_run_at = run_stats.get("last_run_at", "")
        track_count = run_stats.get("last_run_track_count", 0)

        if last_run_status != "ok":
            continue  # Hanya yang run sukses

        try:
            tracks = int(track_count)
        except (ValueError, TypeError):
            tracks = 0

        is_pool = name.startswith("POOL ")
        duration = estimate_duration(tracks, is_pool)
        description = desc_map.get(name, prog.get("description", ""))

        new_rows.append({
            "Program Name": name,
            "Description": description,
            "Spotify URI": playlist_uri,
            "Duration": duration,
            "Last Success Run History": last_run_at or timestamp,
        })

    # 5. Gabung: existing dulu, baru di belakang
    all_rows = existing_rows + new_rows

    # 6. Tulis ulang CSV
    fieldnames = [
        "Program Name",
        "Description",
        "Spotify URI",
        "Duration",
        "Last Success Run History",
    ]
    with SUCCESS_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    print(f"Existing rows: {len(existing_rows)}")
    print(f"New rows added: {len(new_rows)}")
    print(f"Total rows: {len(all_rows)}")
    print(f"Tersimpan ke {SUCCESS_CSV}")


if __name__ == "__main__":
    main()
