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

    # Files to import specifically
    files_to_import = [
        ROOT / "templates" / "TEMPLATE_HOTEL_24H.json",
        ROOT / "programs" / "generated" / "hotel_grand_lobby.json",
        ROOT / "programs" / "generated" / "cafe_des_artistes.json",
        ROOT / "programs" / "generated" / "midnight_rooftop.json",
    ]

    for path in files_to_import:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        name = data.get("name")
        # Check if exists to get PID
        r_list = sm.get("/api/programs/enriched").json()
        pid = next((item.get("pid") for item in r_list if item.get("name") == name), None)

        if pid:
            print(f"Updating {name}...")
            sm.put(f"/api/programs/{pid}", json={"name": name, "program_json": data})
        else:
            print(f"Creating {name}...")
            sm.post("/api/programs/", json={"name": name, "program_json": data})

    # Run only the 3 hotel programs
    hotel_names = [
        "The Grand Lobby — Timeless Elegance",
        "Café des Artistes — Matin à Paris",
        "Midnight Rooftop — Celestial Lounge"
    ]

    # Refresh PIDs
    r_list = sm.get("/api/programs/enriched").json()
    
    for h_name in hotel_names:
        pid = next((item.get("pid") for item in r_list if item.get("name") == h_name), None)
        if pid:
            print(f"Running {h_name}...")
            sm.post(f"/api/programs/{pid}/run", params={"save": "true"})
        else:
            print(f"Could not find PID for {h_name}")

if __name__ == "__main__":
    main()
