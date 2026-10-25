#!/usr/bin/env python3
"""Import all 120 playlist generators + 21 pool programs into SmarterPlaylights
and run them one by one, reusing a single saved Spotify session.

This script does NOT create Spotify playlists by itself — it imports the
program JSON files into SmarterPlaylights and triggers runs. The first run of
each program creates the Spotify playlist via the ``PlaylistSave`` component;
later runs replace it.

Usage:
  python tools/import_run_all.py              # import + run everything (save=true)
  python tools/import_run_all.py --import-only # only import programs, no run
  python tools/import_run_all.py --run-only    # only run already-imported programs
  python tools/import_run_all.py --limit 10    # process first 10 generators only
  python tools/import_run_all.py --delay 3     # seconds between runs
  python tools/import_run_all.py --pools-only  # pools only (21)
  python tools/import_run_all.py --gens-only   # generators only (120)

Outputs:
  config/import_run_log.csv   - one row per program (name, pid, action, run_id, status, tracks, error)
  config/import_run_log.json  - full detail per program

Prerequisites:
  1. python tools/sm_session.py --init   (login once with Spotify)
  2. python tools/generate_programs.py --mode all   (regenerate 120 JSON if needed)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
PROGRAMS_DIR = ROOT / "programs"
POOLS_DIR = PROGRAMS_DIR / "pools"
GENS_DIR = PROGRAMS_DIR / "generated"
AUTH_DIR = ROOT / "auth"

LOG_CSV = CONFIG_DIR / "import_run_log.csv"
LOG_JSON = CONFIG_DIR / "import_run_log.json"

sys.path.insert(0, str(ROOT / "tools"))
from sm_session import SmarterPlaylistsSession  # noqa: E402


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def discover_programs(mode: str) -> list[Path]:
    """Return list of program JSON files to process."""
    files: list[Path] = []
    if mode in ("all", "pools-only") and POOLS_DIR.exists():
        files.extend(sorted(POOLS_DIR.glob("*.json")))
    if mode in ("all", "gens-only") and GENS_DIR.exists():
        files.extend(sorted(GENS_DIR.glob("*.json")))
    return files


def existing_programs(sm: SmarterPlaylistsSession) -> dict[str, str]:
    """Return {program_name: pid} for programs already in SmarterPlaylights."""
    r = sm.get("/api/programs/enriched")
    if not r.ok:
        print(f"[warn] could not list existing programs: HTTP {r.status_code} {r.text[:200]}")
        return {}
    data = r.json()
    out: dict[str, str] = {}
    if isinstance(data, list):
        for item in data:
            name = item.get("name") or item.get("program_name")
            pid = item.get("pid") or item.get("id")
            if name and pid:
                out[str(name)] = str(pid)
    elif isinstance(data, dict):
        for item in data.get("programs", []):
            name = item.get("name")
            pid = item.get("pid") or item.get("id")
            if name and pid:
                out[str(name)] = str(pid)
    return out


def import_program(sm: SmarterPlaylistsSession, path: Path, existing: dict[str, str]) -> dict[str, Any]:
    """Import (or update) one program JSON file. Returns result dict."""
    data = load_json(path)
    name = data.get("name") or path.stem
    program_json = data
    result: dict[str, Any] = {
        "file": path.name,
        "name": name,
        "pid": None,
        "action": None,
        "run_id": None,
        "run_status": None,
        "tracks": None,
        "error": None,
    }

    if name in existing:
        pid = existing[name]
        result["pid"] = pid
        # Update existing program
        r = sm.put(f"/api/programs/{pid}", json={"name": name, "tags": program_json.get("tags", []), "program_json": program_json})
        if r.ok:
            result["action"] = "updated"
        else:
            result["error"] = f"update failed HTTP {r.status_code}: {r.text[:200]}"
            return result
    else:
        r = sm.post("/api/programs/", json={"name": name, "tags": program_json.get("tags", []), "program_json": program_json})
        if r.ok:
            created = r.json()
            pid = created.get("pid") or created.get("id") or created.get("program", {}).get("pid")
            result["pid"] = str(pid) if pid else None
            result["action"] = "created"
        else:
            result["error"] = f"create failed HTTP {r.status_code}: {r.text[:200]}"
            return result

    return result


def run_program(sm: SmarterPlaylistsSession, pid: str, save: bool = True) -> dict[str, Any]:
    """Run one program and poll until complete/error. Returns result dict."""
    result: dict[str, Any] = {"run_id": None, "run_status": None, "tracks": None, "error": None}

    r = sm.post(f"/api/programs/{pid}/run", params={"save": "true" if save else "false"})
    if not r.ok:
        result["error"] = f"run failed HTTP {r.status_code}: {r.text[:200]}"
        return result
    payload = r.json()
    run_id = payload.get("run_id") or payload.get("id")
    result["run_id"] = str(run_id) if run_id else None
    if not run_id:
        result["error"] = f"no run_id in response: {r.text[:200]}"
        return result

    # Poll status (max ~5 minutes)
    for _ in range(300):
        time.sleep(2)
        rs = sm.get(f"/api/runs/{run_id}/status")
        if not rs.ok:
            result["error"] = f"status poll failed HTTP {rs.status_code}"
            return result
        st = rs.json()
        status = st.get("status")
        result["run_status"] = status
        if status == "complete":
            result["tracks"] = (st.get("tracks") or [])
            if isinstance(result["tracks"], list):
                result["tracks"] = len(result["tracks"])
            return result
        if status in ("error", "failed", "cancelled"):
            result["error"] = st.get("error") or f"run ended with status {status}"
            return result
    result["error"] = "run polling timed out"
    return result


def write_logs(rows: list[dict[str, Any]]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["file", "name", "pid", "action", "run_id", "run_status", "tracks", "error"]
    with LOG_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    with LOG_JSON.open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2, ensure_ascii=False)
    print(f"\nLog written to {LOG_CSV} and {LOG_JSON}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Import and run all SmarterPlaylights programs")
    ap.add_argument("--import-only", action="store_true", help="only import programs, do not run")
    ap.add_argument("--run-only", action="store_true", help="only run already-imported programs")
    ap.add_argument("--limit", type=int, default=0, help="process at most N generator files")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between runs")
    ap.add_argument("--pools-only", action="store_true", help="pools only (21)")
    ap.add_argument("--gens-only", action="store_true", help="generators only (120)")
    ap.add_argument("--no-save", action="store_true", help="preview runs without saving to Spotify")
    args = ap.parse_args()

    mode = "all"
    if args.pools_only:
        mode = "pools-only"
    if args.gens_only:
        mode = "gens-only"

    sm = SmarterPlaylistsSession()
    try:
        sm.load()  # raises if no valid session
    except RuntimeError as exc:
        print(str(exc))
        print("Run first:  python tools/sm_session.py --init")
        sys.exit(1)

    files = discover_programs(mode)
    if args.limit and args.limit > 0:
        files = files[: args.limit]

    print(f"Found {len(files)} program file(s) (mode={mode})")

    existing = existing_programs(sm)
    print(f"Existing programs in SmarterPlaylights: {len(existing)}")

    rows: list[dict[str, Any]] = []

    # ---- Import phase ---------------------------------------------------- #
    if not args.run_only:
        for path in files:
            res = import_program(sm, path, existing)
            rows.append(res)
            status = res["action"] or ("ERROR" if res["error"] else "OK")
            print(f"[{status}] {res['name']}  ({res['file']})  pid={res['pid']}")
            if res["error"]:
                print(f"      ! {res['error']}")
            # refresh existing cache so updates don't re-create
            if res["pid"]:
                existing[res["name"]] = res["pid"]

    # ---- Run phase ------------------------------------------------------- #
    if not args.import_only:
        to_run = [r for r in rows if r["pid"] and not r["error"]]
        print(f"\nRunning {len(to_run)} program(s) (save={'false' if args.no_save else 'true'})...")
        for i, res in enumerate(to_run, 1):
            print(f"[{i}/{len(to_run)}] run {res['name']} (pid={res['pid']}) ...", end=" ")
            run_res = run_program(sm, res["pid"], save=not args.no_save)
            res["run_id"] = run_res["run_id"]
            res["run_status"] = run_res["run_status"]
            res["tracks"] = run_res["tracks"]
            res["error"] = run_res["error"]
            ok = "OK" if run_res["run_status"] == "complete" and not run_res["error"] else "FAIL"
            print(f"{ok}  status={run_res['run_status']} tracks={run_res['tracks']}")
            if run_res["error"]:
                print(f"      ! {run_res['error']}")
            if i < len(to_run) and args.delay > 0:
                time.sleep(args.delay)

    write_logs(rows)

    done = sum(1 for r in rows if r.get("run_status") == "complete")
    fail = sum(1 for r in rows if r.get("error"))
    print(f"\nSummary: {len(rows)} processed, {done} completed, {fail} failed.")


if __name__ == "__main__":
    main()
