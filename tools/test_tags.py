#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from sm_session import SmarterPlaylistsSession

def main():
    sm = SmarterPlaylistsSession()
    try:
        sm.load()
    except Exception as e:
        print(f"Session error: {e}")
        return

    # 1. Find a program to test
    # Let's use POOL Priority
    prog_path = ROOT / "programs" / "pools" / "pool_priority.json"
    if not prog_path.exists():
        print(f"Could not find {prog_path}")
        return
    
    with open(prog_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    name = data.get("name")
    tags = data.get("tags", ["test-tag-1", "test-tag-2"])
    
    # 2. Get the PID for this program from the API
    r_list = sm.get("/api/programs/enriched")
    pid = None
    for item in r_list.json():
        if item.get("name") == name:
            pid = item.get("pid")
            break
    
    if not pid:
        print(f"Could not find PID for {name}")
        return
    
    print(f"Testing update for {name} (pid: {pid})")
    print(f"Sending tags: {tags}")
    
    # 3. Try the update
    # Try different payload structures
    payload = {
        "name": name,
        "tags": tags,
        "program_json": data
    }
    
    r_update = sm.put(f"/api/programs/{pid}", json=payload)
    
    if r_update.ok:
        print("Successfully sent PUT request!")
        # 4. Verify immediately
        r_verify = sm.get(f"/api/programs/{pid}")
        print("Server response for verification:")
        print(json.dumps(r_verify.json(), indent=2))
    else:
        print(f"Update failed HTTP {r_update.status_code}")
        print(f"Response: {r_update.text}")

if __name__ == "__main__":
    main()
