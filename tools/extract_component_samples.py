#!/usr/bin/env python3
"""Extract one representative spec per component type from generated programs.

The output is used for a read-only call to SmarterPlaylists
POST /api/programs/validate-component. It does not create or import anything.

Usage:
  python tools/extract_component_samples.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = ROOT / "programs"
OUTPUT = PROGRAMS_DIR / "component_samples.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def compact_sample(component_type: str, params: dict[str, Any]) -> dict[str, Any]:
    params = dict(params)
    if component_type == "TrackSource":
        params["uris"] = " ".join(str(params.get("uris", "")).split()[:3])
    elif component_type == "ArtistURIs":
        params["uris"] = " ".join(str(params.get("uris", "")).split()[:2])
    elif component_type == "SimpleArtistFilter":
        names = [name.strip() for name in str(params.get("artistNames", "")).split(",") if name.strip()]
        params["artistNames"] = ", ".join(names[:2])
    elif component_type == "SpotifyPlaylist":
        params["uri"] = "spotify:playlist:61125e02nVEg0kti79j0DO"
        params["name"] = "eL Utama"
        params["user"] = ""
    return {"type": component_type, "params": params}


def main() -> None:
    samples: dict[str, dict[str, Any]] = {}
    files = sorted((PROGRAMS_DIR / "pools").glob("*.json")) + sorted((PROGRAMS_DIR / "generated").glob("*.json"))
    for path in files:
        program = load_json(path)
        for component in program.get("components", {}).values():
            component_type = component.get("type")
            if not component_type or component_type in samples:
                continue
            samples[component_type] = compact_sample(component_type, component.get("params", {}))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(samples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"file": str(OUTPUT), "component_types": len(samples), "types": sorted(samples)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
