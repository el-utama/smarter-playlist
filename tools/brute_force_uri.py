#!/usr/bin/env python3
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEAD_URI = "0vM7A1N8zP6L0SjS4P2Q9k"
NEW_URI = "75Tnr3Zvc0ysnUtBkNNf6n"

def main():
    updated_count = 0
    for path in ROOT.rglob("*.json"):
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            
            if DEAD_URI in content:
                new_content = content.replace(DEAD_URI, NEW_URI)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                updated_count += 1
        except Exception as e:
            print(f"Error processing {path}: {e}")

    print(f"Brute force replaced {updated_count} files.")

if __name__ == "__main__":
    main()
