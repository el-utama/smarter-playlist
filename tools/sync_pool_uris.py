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

    # 1. Get all current URIs from the API
    print("Fetching latest URIs from SmarterPlaylists...")
    r = sm.get("/api/programs/enriched")
    if not r.ok:
        print(f"Failed to fetch enriched programs: {r.status_code}")
        return
    
    enriched_data = r.json()
    uri_map = {}
    for prog in enriched_data:
        name = prog.get("name")
        uri = prog.get("playlist_uri")
        if name and uri:
            uri_map[name] = uri

    print(f"Captured {len(uri_map)} URIs.")

    # 2. Update all local files
    updated_count = 0
    # We look for any JSON file that might contain a pool URI
    for path in ROOT.rglob("*.json"):
        if "manifest.json" in path.name:
            continue
            
        with open(path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        
        changed = False
        # We check for every pool name in the file and replace its URI if we found a new one
        # The format in JSON is usually "uri": "spotify:playlist:..."
        # But we can just iterate through the uri_map and replace values if we find the name in the file
        
        # Better way: parse JSON, find SpotifyPlaylist components, and update based on 'name'
        try:
            data = json.load(f)
            if "components" in data:
                for comp_id, comp in data["components"].items():
                    if comp.get("type") == "SpotifyPlaylist":
                        pool_name = comp.get("params", {}).get("name")
                        if pool_name in uri_map:
                            new_uri = uri_map[pool_name]
                            if comp["params"].get("uri") != new_uri:
                                comp["params"]["uri"] = new_uri
                                changed = True
            
            if changed:
                with open(path, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out, indent=2, ensure_ascii=False)
                updated_count += 1
        except json.JSONDecodeError:
            continue

    print(f"Updated {updated_count} files with the latest verified URIs.")

if __name__ == "__main__":
    main()
