#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = ROOT / "programs"

def main():
    # Get all generator files (excluding pools)
    gens = sorted([f for f in os.listdir(PROGRAMS_DIR) if f.endswith(".json") and "pool" not in f])
    
    batch_size = 30
    for i in range(0, len(gens), batch_size):
        batch = gens[i : i + batch_size]
        print(f"\n>>> Processing batch {i//batch_size + 1} ({i} to {i+len(batch)})")
        
        # We use a modified version of the import logic by calling a temporary script 
        # or just modifying the files in the directory temporarily.
        # Easier: create a temporary directory with only the current batch.
        batch_dir = ROOT / "programs_batch"
        batch_dir.mkdir(exist_ok=True)
        
        # Clear previous batch
        for f in batch_dir.glob("*.json"):
            f.unlink()
            
        # Copy current batch
        for f_name in batch:
            (PROGRAMS_DIR / f_name).replace(batch_dir / f_name)
            
        try:
            # Run the import script pointing to the batch directory
            # We need to override the programs directory in the script or pass it as an env var
            # Since import_run_all.py uses a hardcoded path, we'll temporarily move the 
            # original programs folder and replace it with the batch folder.
            
            # Backup original
            orig_dir = ROOT / "programs"
            backup_dir = ROOT / "programs_backup"
            if backup_dir.exists():
                # This is a bit messy. Let's just use a different approach.
                pass
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
