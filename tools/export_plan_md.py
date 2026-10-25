#!/usr/bin/env python3
"""Export a human-readable Markdown plan from the local config.

Usage:
  python tools/export_plan_md.py

Output:
  config/plan_120.md
  config/playlist_copy_120.md
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
OUTPUT = CONFIG_DIR / "plan_120.md"
COPY_OUTPUT = CONFIG_DIR / "playlist_copy_120.md"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> None:
    playlists_doc = load_json(CONFIG_DIR / "playlists_120.draft.json")
    pool_uris = load_json(CONFIG_DIR / "pool_uris.json")

    categories = playlists_doc["categories"]
    pools = playlists_doc["pools"]
    playlists = playlists_doc["playlists"]

    lines: list[str] = []
    lines.append("# Rencana 120 Playlist")
    lines.append("")
    lines.append(
        "> Dokumen ini dihasilkan dari `config/playlists_120.draft.json`. "
        "Taxonomy sudah disetujui (2026-10-24). Judul dan deskripsi playlist memakai bahasa Inggris. "
        "Belum ada playlist atau program yang dibuat/diimpor/dijalankan."
    )
    lines.append("")
    lines.append("## Ringkasan")
    lines.append("")
    lines.append("| Item | Nilai |")
    lines.append("|---|---|")
    lines.append(f"| Kategori | {len(categories)} |")
    lines.append(f"| Genre | {sum(len(c['genres']) for c in categories.values())} |")
    lines.append(f"| Mood | {sum(len(c['moods']) for c in categories.values())} |")
    lines.append(f"| Playlist | {len(playlists)} |")
    lines.append(f"| Pool | {len(pools)} |")
    lines.append(f"| Batas durasi | 6 jam (21.600 detik) |")
    lines.append(f"| Rotasi | 60% priority / 40% global |")
    lines.append(f"| Priority artist | 26 (25 No Detours + eL Utama) |")
    lines.append(f"| Bahasa judul & deskripsi | English (marketable, professional) |")
    lines.append("")
    lines.append("## Format judul & deskripsi")
    lines.append("")
    lines.append("- **Judul:** `{Category} {index:02d} — {Genre} · {Mood}` — contoh: `Morning 01 — Acoustic & Folk · Fresh`.")
    lines.append(
        "- **Deskripsi:** category intro + mood/genre + artist-first picks + `Refreshed regularly.` "
        "Variable `${NUM_TRACKS}` dan `${DURATION}` diisi otomatis oleh SmarterPlaylists."
    )
    lines.append("")
    lines.append("| Kategori | Contoh judul | Contoh deskripsi |")
    lines.append("|---|---|---|")
    for category_key in ["pagi", "siang", "sore", "malam"]:
        first = next(playlist for playlist in playlists if playlist["category"] == category_key)
        lines.append(
            f"| {categories[category_key]['label']} | {first['name']} | {first['description']} |"
        )
    lines.append("")

    lines.append("## 21 Pool")
    lines.append("")
    lines.append("| Pool | Tipe | Kategori | Genre | Hard filter | Artist genre | Explicit | URI |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for pool in pools:
        uri = pool_uris.get(pool["program_name"], "")
        uri_status = "terisi" if uri and "REPLACE_ME" not in uri else "placeholder"
        lines.append(
            "| {name} | {type} | {category} | {genre} | {filter} | {artist_genre} | {explicit} | {uri} |".format(
                name=pool["program_name"],
                type=pool["type"],
                category=pool.get("category_label", ""),
                genre=pool.get("genre", ""),
                filter=pool.get("genre_filter") or "(off)",
                artist_genre=pool.get("artist_genre") or "-",
                explicit=pool.get("explicit_mode", ""),
                uri=uri_status,
            )
        )
    lines.append("")

    for category_key in ["pagi", "siang", "sore", "malam"]:
        category = categories[category_key]
        lines.append(f"## {category['label']} — 30 Playlist")
        lines.append("")
        lines.append("| No | Nama | Genre | Mood | Explicit | Priority offset | Global offset |")
        lines.append("|---|---|---|---|---|---|---|")
        for playlist in playlists:
            if playlist["category"] != category_key:
                continue
            lines.append(
                "| {index:02d} | {name} | {genre} | {mood} | {explicit} | {priority_offset} | {global_offset} |".format(
                    index=playlist["index"],
                    name=playlist["name"],
                    genre=playlist["genre"],
                    mood=playlist["mood"],
                    explicit=playlist["explicit_mode"],
                    priority_offset=playlist["priority_offset"],
                    global_offset=playlist["global_offset"],
                )
            )
        lines.append("")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    copy_lines: list[str] = []
    copy_lines.append("# Playlist Copy — 120")
    copy_lines.append("")
    copy_lines.append(
        "> English titles and descriptions for review. Generated from "
        "`config/playlists_120.draft.json`. No playlist has been created yet. "
        "Variables `${NUM_TRACKS}` and `${DURATION}` are filled automatically at run time."
    )
    copy_lines.append("")
    for category_key in ["pagi", "siang", "sore", "malam"]:
        category = categories[category_key]
        copy_lines.append(f"## {category['label']} — 30 Playlist")
        copy_lines.append("")
        for playlist in playlists:
            if playlist["category"] != category_key:
                continue
            copy_lines.append(f"### {playlist['name']}")
            copy_lines.append(
                f"**Genre:** {playlist['genre']} · **Mood:** {playlist['mood']} · "
                f"**Explicit:** {playlist['explicit_mode']}"
            )
            copy_lines.append("")
            copy_lines.append(playlist["description"])
            copy_lines.append("")
    COPY_OUTPUT.write_text("\n".join(copy_lines).rstrip() + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "file": str(OUTPUT),
                "copy_file": str(COPY_OUTPUT),
                "playlists": len(playlists),
                "pools": len(pools),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
