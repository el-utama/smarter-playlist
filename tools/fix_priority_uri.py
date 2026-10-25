#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_PRIORITY_URI = "spotify:playlist:75Tnr3Zvc0ysnUtBkNNf6n"
OLD_PRIORITY_URI = "spotify:playlist:01L39CjL3P6z0Tz7p4n7Nq"

def update_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    
    if OLD_PRIORITY_URI in content:
        new_content = content.replace(OLD_PRIORITY_URI, NEW_PRIORITY_URI)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    updated_count = 0
    # Update all JSONs in programs/ and templates/
    for path in ROOT.rglob("*.json"):
        if update_file(path):
            updated_count += 1
            
    print(f"Successfully updated {updated_count} files with the new Priority Pool URI.")

if __name__ == "__main__":
    main()
