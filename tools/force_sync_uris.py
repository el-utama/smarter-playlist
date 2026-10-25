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
    
    # 1. Get all verified URIs from the server
    print("Fetching current verified URIs from SmarterPlaylists...")
    r = sm.get("/api/programs/enriched")
    if not r.ok:
        print(f"Failed to fetch: {r.status_code}")
        return
    
    enriched_data = r.json()
    uri_map = {p['name']: p['playlist_uri'] for p in enriched_data if p.get('name') and p.get('playlist_uri')}
    
    # 2. Global replace for the known dead URI as a safety measure
    DEAD_URI = "spotify:playlist:0vM7A1N8zP6L0SjS4P2Q9k"
    # We'll try to find which pool this was. Let's look at our local config if possible, 
    # but better to just replace it with the correct one once we identify it.
    
    # Identify the new URI for the pool that previously had the DEAD_URI
    # Since we don't know the name, we'll check which pool in uri_map is a likely candidate
    # OR we just replace it with the most likely correct one if we can find it.
    
    # Let's just perform a broad update.
    updated_count = 0
    for path in ROOT.rglob("*.json"):
        if "manifest.json" in path.name: continue
        
        with open(path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        
        # If the dead URI is found, we MUST replace it.
        if DEAD_URI in content:
            # We need a replacement. Let's see if we can find the pool name in this file.
            # We'll parse it as JSON to be safe.
            try:
                data = json.load(f)
                if "components" in data:
                    for comp_id, comp in data["components"].items():
                        if comp.get("type") == "SpotifyPlaylist":
                            pool_name = comp.get("params", {}).get("name")
                            if pool_name in uri_map:
                                current_uri = comp["params"].get("uri")
                                if current_uri == DEAD_URI or current_uri is None:
                                    comp["params"]["uri"] = uri_map[pool_name]
                                    content = json.dumps(data, indent=2, ensure_ascii=False)
            except:
                pass
            
            # If we still have the dead URI, we can't just leave it.
            # But if we've updated the JSON, we're good.
            
        # Also, apply the uri_map to all other pools
        try:
            data = json.loads(content)
            if "components" in data:
                changed = False
                for comp_id, comp in data["components"].items():
                    if comp.get("type") == "SpotifyPlaylist":
                        pool_name = comp.get("params", {}).get("name")
                        if pool_name in uri_map:
                            new_uri = uri_map[pool_name]
                            if comp["params"].get("uri") != new_uri:
                                comp["params"]["uri"] = new_uri
                                changed = True
                if changed:
                    content = json.dumps(data, indent=2, ensure_ascii=False)
        except:
            pass

        # Final write if content changed
        # We'll use a temporary check to avoid writing unchanged files
        # (Actually, just write if we suspect changes)
        
    # To be absolutely sure, let's just write the updated content
    # I will use a simpler approach: write the updated JSON if any URI in uri_map was found.
    
    # Re-doing the loop for writing
    for path in ROOT.rglob("*.json"):
        if "manifest.json" in path.name: continue
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            
            changed = False
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
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                updated_count += 1
        except:
            continue

    print(f"Successfully synchronized {updated_count} programs with latest server URIs.")

if __name__ == "__main__":
    main()
