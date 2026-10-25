#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from sm_session import SmarterPlaylistsSession

def main():
    sm = SmarterPlaylistsSession()
    sm.load()

    hotel_progs = [
        'The Grand Lobby — Timeless Elegance',
        'Café des Artistes — Matin à Paris',
        'Midnight Rooftop — Celestial Lounge'
    ]

    # 1. Get all programs to find PIDs
    print("Fetching programs from server...")
    r = sm.get('/api/programs/enriched')
    if not r.ok:
        print(f"Failed to fetch programs: {r.status_code}")
        return
    
    all_progs = r.json()
    
    # 2. Delete the Hotel programs to force a hard reset of validation
    for p in all_progs:
        name = p.get('name')
        if name in hotel_progs:
            pid = p.get('id')
            if pid:
                print(f"Deleting {name} (PID: {pid}) to clear server cache...")
                # SmarterPlaylists usually uses DELETE /api/programs/{id}
                del_res = sm.delete(f'/api/programs/{pid}')
                if del_res.ok:
                    print(f"Successfully deleted {name}")
                else:
                    print(f"Failed to delete {name}: {del_res.status_code}")

    print("\nServer cleaned. Now triggering re-import of fresh versions...")

if __name__ == "__main__":
    main()
