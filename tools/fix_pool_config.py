#!/usr/bin/env python3
"""Otomasi perbaikan konfigurasi pool berdasarkan hasil impor/run.

Membaca config/import_run_log.csv, mengidentifikasi program pool (nama dimulai
dengan "POOL "), mencari ukuran pool terkecil, lalu memperbarui
global_pool_size_estimate di config/rules.json menjadi angka yang aman agar
offset global (index-1) × 300 mod global_pool_size_estimate tidak menghasilkan
slice kosong di playlist generator.

Tanpa ini, playlist yang menggunakan pool kecil (mis. Morning - Classical &
Piano dengan 45 track) akan mendapat slice kosong karena offset 2700 >> 45.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
LOG_CSV = CONFIG_DIR / "import_run_log.csv"
RULES_JSON = CONFIG_DIR / "rules.json"

# Pool dengan ukuran di bawah ambang ini dianggap terlalu kecil dan perlu
# perhatian tambahan (bukan hanya disetel estimate).
SMALL_POOL_THRESHOLD = 200


def load_log() -> list[dict[str, str]]:
    with LOG_CSV.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def pool_sizes(rows: list[dict[str, str]]) -> list[tuple[str, int]]:
    """Kembalikan [(nama_pool, jumlah_track)] untuk baris pool yang complete."""
    out: list[tuple[str, int]] = []
    for r in rows:
        name = (r.get("name") or "").strip()
        status = (r.get("run_status") or "").strip()
        if not name.startswith("POOL "):
            continue
        if status != "complete":
            continue
        try:
            tracks = int(r.get("tracks") or 0)
        except ValueError:
            tracks = 0
        out.append((name, tracks))
    return out


def update_rules(new_estimate: int, dry_run: bool = False) -> dict:
    with RULES_JSON.open("r", encoding="utf-8-sig") as fh:
        rules = json.load(fh)

    old = rules.get("global_pool_size_estimate")
    result = {
        "old": old,
        "new": new_estimate,
        "changed": old != new_estimate,
        "file": str(RULES_JSON),
    }

    if result["changed"] and not dry_run:
        rules["global_pool_size_estimate"] = new_estimate
        with RULES_JSON.open("w", encoding="utf-8") as fh:
            json.dump(rules, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    elif result["changed"] and dry_run:
        print(f"[dry-run] rules.json: global_pool_size_estimate {old} -> {new_estimate}")

    return result


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description="Otomasi perbaikan global_pool_size_estimate dari log impor pool."
    )
    ap.add_argument("--apply", action="store_true", help="Tulis perubahan ke config/rules.json")
    ap.add_argument(
        "--threshold",
        type=int,
        default=SMALL_POOL_THRESHOLD,
        help="Ambang pool kecil yang perlu perhatian tambahan",
    )
    args = ap.parse_args()

    if not LOG_CSV.exists():
        print(f"File log tidak ditemukan: {LOG_CSV}")
        print("Jalankan dulu: python tools/import_run_all.py")
        sys.exit(1)

    rows = load_log()
    sizes = pool_sizes(rows)

    if not sizes:
        print("Tidak ada data pool yang ditemukan di log impor.")
        sys.exit(1)

    print("Ukuran pool hasil run:")
    for name, tracks in sorted(sizes, key=lambda x: x[1]):
        flag = "  <-- KECIL" if tracks < args.threshold else ""
        print(f"  {name:<45} {tracks:>5} tracks{flag}")

    min_name, min_size = min(sizes, key=lambda x: x[1])
    small = [n for n, t in sizes if t < args.threshold]

    print(f"\nPool terkecil: {min_name} ({min_size} track)")
    if small:
        print(f"Pool di bawah ambang {args.threshold}: {', '.join(small)}")

    # Hitung estimate aman: gunakan ukuran pool terkecil agar offset modulo
    # selalu menghasilkan slice non-kosong (asalkan slice <= ukuran pool).
    safe_estimate = min_size

    result = update_rules(safe_estimate, dry_run=not args.apply)

    if result["changed"]:
        print(
            f"\nglobal_pool_size_estimate: {result['old']} -> {result['new']}"
        )
        if args.apply:
            print(f"Disimpan ke {result['file']}")
        else:
            print("(dry-run, gunakan --apply untuk menyimpan)")
    else:
        print(f"\nglobal_pool_size_estimate sudah {result['old']}, tidak perlu diubah.")

    if small:
        print(
            "\nCatatan: Beberapa pool masih kecil. Untuk memperbaiki secara permanent, "
            "longgarkan filter pada template pool terkait di templates/ lalu jalankan "
            "generate_programs.py --mode pools-only --clean, impor ulang pool, dan jalankan "
            "ulang fix_pool_config.py --apply."
        )


if __name__ == "__main__":
    main()
