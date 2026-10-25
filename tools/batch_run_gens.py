#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = ROOT / "programs"
BACKUP_DIR = ROOT / "programs_backup"

def main():
    # 1. Backup all programs to a safe place
    if not BACKUP_DIR.exists():
        shutil.copytree(PROGRAMS_DIR, BACKUP_DIR)
        print(f"Backed up programs to {BACKUP_DIR}")

    # Get all generator files (excluding pools)
    all_files = sorted([f for f in os.listdir(PROGRAMS_DIR) if f.endswith(".json")])
    gens = [f for f in all_files if "pool" not in f]
    
    batch_size = 30
    total_gens = len(gens)
    
    for i in range(0, total_gens, batch_size):
        batch = gens[i : i + batch_size]
        print(f"\n{'='*60}\nProcessing Batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, total_gens)} of {total_gens})\n{'='*60}")
        
        # Temporary directory for the current batch
        tmp_programs = ROOT / "programs_tmp"
        if tmp_programs.exists():
            shutil.rmtree(tmp_programs)
        tmp_programs.mkdir()
        
        # Copy ONLY the current batch into the programs folder 
        # (Actually, the import script reads from 'programs/', so we swap)
        
        # Swap: programs -> programs_tmp, programs_tmp -> programs
        # But wait, just move the batch files into the folder and remove others
        # Even better: Use the backup to restore and then delete non-batch files
        
        # Restore from backup
        if PROGRAMS_DIR.exists():
            shutil.rmtree(PROGRAMS_DIR)
        shutil.copytree(BACKUP_DIR, PROGRAMS_DIR)
        
        # Remove everything NOT in the current batch
        # Keep pools because generators need them!
        for f in os.listdir(PROGRAMS_DIR):
            path = PROGRAMS_DIR / f
            if path.is_dir():
                continue
            if "pool" in f:
                continue
            if f not in batch:
                path.unlink()
        
        # Run import_run_all.py
        try:
            subprocess.run(["python", "tools/import_run_all.py", "--gens-only"], 
                           cwd=ROOT, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Batch {i//batch_size + 1} failed: {e}")

    # Restore everything to original state
    if PROGRAMS_DIR.exists():
        shutil.rmtree(PROGRAMS_DIR)
    shutil.copytree(BACKUP_DIR, PROGRAMS_DIR)
    print("\nRestored all programs to the programs folder.")

if __name__ == "__main__":
    main()
