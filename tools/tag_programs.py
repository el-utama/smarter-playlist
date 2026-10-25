#!/usr/bin/env python3
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = ROOT / "programs"

# Mapping for Time-of-Day
TIME_MAP = {
    "Morning": "morning",
    "Midday": "midday",
    "Afternoon": "afternoon",
    "Night": "night",
}

# Mapping for Moods/Vibes
MOOD_MAP = {
    "Fresh": "fresh",
    "Calm": "calm",
    "Hopeful": "hopeful",
    "Warm": "warm",
    "Focused": "focused",
    "Gentle": "gentle",
    "Upbeat": "upbeat",
    "Energetic": "energetic",
    "Confident": "confident",
    "Bright": "bright",
    "Groovy": "groovy",
    "Motivational": "motivational",
    "Sleepy": "sleepy",
    "Dreamy": "dreamy",
    "Melancholic": "melancholic",
    "Intimate": "intimate",
    "Cinematic": "cinematic",
    "Nocturnal": "nocturnal",
    "Mellow": "mellow",
    "Romantic": "romantic",
    "Nostalgic": "nostalgic",
    "Relaxed": "relaxed",
    "Golden": "golden",
    "Reflective": "reflective",
}

# Mapping for Thematic
THEME_MAP = {
    "Golden Hour": "thematic",
    "Quiet Hour": "thematic",
    "Midnight": "thematic",
    "Special": "thematic",
}

def main():
    # Find all json programs
    # We look in both 'generated' and any other folders in 'programs/'
    all_program_files = []
    for path in PROGRAMS_DIR.rglob("*.json"):
        if path.name == "manifest.json" or path.name == "component_samples.json":
            continue
        all_program_files.append(path)

    print(f"Found {len(all_program_files)} program files. Applying tags...\n")

    updated_count = 0

    for file_path in all_program_files:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding {file_path}, skipping.")
                continue

        name = data.get("name", "")
        tags = set()

        # 1. Primary Category Tag
        if "POOL " in name:
            tags.add("pool")
        elif "Discography" in name or "No Detours" in name:
            tags.add("discography")
        elif any(word in name for word in ["Morning", "Midday", "Afternoon", "Night"]):
            # If it's not a pool, it's a generator
            tags.add("generator")
        
        # Check for thematic programs
        for theme_key, tag_val in THEME_MAP.items():
            if theme_key in name:
                tags.add(tag_val)

        # 2. Time-of-Day Tags
        for time_key, tag_val in TIME_MAP.items():
            if time_key in name:
                tags.add(tag_val)

        # 3. Mood Tags
        for mood_key, tag_val in MOOD_MAP.items():
            if mood_key in name:
                tags.add(tag_val)

        # 4. Priority/Special Tags
        if "Priority" in name or "No Detours" in name:
            tags.add("priority")
        
        # 5. Technical Tag
        tags.add("playable-verified")

        # Update JSON
        # Convert set to sorted list for consistency
        final_tags = sorted(list(tags))
        
        if data.get("tags") != final_tags:
            data["tags"] = final_tags
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            updated_count += 1
            # print(f"Updated {name} -> {final_tags}")

    print(f"\nDone! Updated {updated_count} programs with consistent tags.")
    print("Now run 'python tools/import_run_all.py' to sync tags to SmarterPlaylists.")

if __name__ == "__main__":
    main()
