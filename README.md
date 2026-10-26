# 🎵 Smart Playlist Ecosystem (120+ Programs)

A professional-grade automation system for SmarterPlaylists, designed to generate high-rotation, high-quality Spotify playlists across multiple categories and moods.

## 🚀 System Architecture

This project implements a scalable "Pool & Generator" architecture:
- **Pools (21):** Specialized source playlists (Priority, Genre, Mood) that act as curated buffers.
- **Generators (120):** Complex programs that slice these pools and sequence them using Multi-Objective Sequencing (MOS) for professional listening.
- **Hotel/Cafe Showcase (3):** High-duration (24h) luxury programs for commercial environments.

## 🛠️ Technology Stack & Systems

### 🏗️ Core Platform
- **SmarterPlaylists:** The primary engine used for playlist logic, filtering, and Spotify API orchestration.
- **Spotify API:** Used for track metadata, playlist creation, and URI management.

### 💻 Automation & Tooling
- **Python 3:** The core language used for all automation scripts.
- **SmarterPlaylists API:** Custom integration via `sm_session.py` to handle OAuth cookies and bulk program management.
- **JSON:** The primary data format for program configuration and templates.
- **Git & GitHub:** Version control for program templates and automation logic.

### 🧠 Sequencing Logic
- **Multi-Objective Sequencer (MOS):** Used to achieve "Comfort Listening" by smoothing energy/valence transitions and enforcing strict artist separation.
- **Rotation Algorithm:** A 60% Priority / 40% Global pool distribution to ensure a balance between core brand identity and variety.

## 📋 Technical Specifications

### Rotation & Logic
- **Priority Ratio:** 60% Priority Pool / 40% Global Pool.
- **Duration Caps:** 
  - Standard: 6 Hours (21,600s)
  - Hotel/Cafe: 24 Hours (86,400s)
- **Constraints:** Strict "No Consecutive Artist" separation.
- **Quality Control:** Integrated `Playable Filter` nodes in every pipeline to ensure 0% dead tracks.

### 🏷️ Tagging Taxonomy
Every program is tagged for easy management in the SmarterPlaylists dashboard:
- `discography` / `pool` / `generator` / `thematic`
- **Time-of-Day:** `morning`, `midday`, `afternoon`, `night`
- **Mood-based:** Professional mood tags per category.

## 📂 Project Structure

```text
├── config/                 # Global rotation rules and successful run logs
├── exports/                # CSV exports of artists and discographies
├── knowledge/              # Technical documentation and MOS recipes
├── programs/
│   ├── generated/          # The 120+ generator JSON files
│   └── pools/              # The 21 source pool JSON files
├── templates/              # Master templates for creating new programs
└── tools/                  # Automation scripts for import, sync, and repair
```

## ⚙️ Setup & Maintenance

### 1. Importing Programs
To import all programs and trigger a run:
```bash
python tools/import_run_all.py
```

### 2. Synchronizing URIs
If a source pool URI changes, run the sync tool to update all 120+ generators automatically:
```bash
python tools/sync_pool_uris.py
```

### 3. Updating the Priority Pool
The Priority Pool is the heart of the system. To rebuild it and propagate the new URI:
1. Run the `POOL Priority` program in SmarterPlaylists.
2. Run `tools/sync_pool_uris.py`.
3. Run `tools/import_run_all.py --import-only`.

## 🏨 Hotel Showcase Programs
Specialized 24-hour programs designed for luxury environments:
- **The Grand Lobby** — Timeless Elegance
- **Café des Artistes** — Matin à Paris
- **Midnight Rooftop** — Celestial Lounge

---
*Developed for professional music curation via SmarterPlaylists.*
