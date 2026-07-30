#!/usr/bin/env python3
"""
set-asset.py — plug a custom-built 3D model into Sam's World-folio.

Copies your .glb/.gltf file from anywhere on your computer into the
project's assets/ folder and registers it in assets/manifest.json.
The game then loads it instead of the built-in procedural model.

Usage:
  python3 set-asset.py --list                    show every slot + status
  python3 set-asset.py <slot> <path-to-model>    install a custom model
  python3 set-asset.py --remove <slot>           go back to the built-in model

Examples:
  python3 set-asset.py island-home ~/Blender/exports/my-home-isle.glb
  python3 set-asset.py npc-bloop "/Users/wang/Downloads/whale v2.glb"
  python3 set-asset.py --remove island-home

There are also per-asset shortcuts in scripts/, e.g.:
  ./scripts/set-home-isle.sh ~/Blender/exports/my-home-isle.glb

After installing, refresh the browser (Cmd+R). Sizing/orientation
conventions for each slot are documented in ASSETS.md.
"""

import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"

# slot -> (subfolder, description)
SLOTS = {
    # islands (replaces terrain + props; label/dialogue/teleport kept)
    "island-home":    ("islands", "Home Isle — about me (grass)"),
    "island-signal":  ("islands", "Signal Peaks — project 01 (mountains)"),
    "island-crypto":  ("islands", "Crypto Cove — project 02 (beach)"),
    "island-skills":  ("islands", "Toolbox Tundra — skills (snow)"),
    "island-contact": ("islands", "Hello Harbor — contact (lighthouse)"),
    # npcs (replaces the model; bobbing/dialogue/voice kept)
    "npc-kappy":      ("npcs", "Kappy the Turtle"),
    "npc-gully":      ("npcs", "Gully the Seagull (incl. buoy)"),
    "npc-bloop":      ("npcs", "Bloop the Whale"),
    "npc-iggy":       ("npcs", "Iggy the Penguin (incl. ice floes)"),
    # props (replaces every placed instance of that type)
    "prop-tree":      ("props", "Round tree (all islands, incl. autumn recolors)"),
    "prop-palm":      ("props", "Palm tree (Crypto Cove)"),
    "prop-snowtree":  ("props", "Snowy tree (Toolbox Tundra)"),
    "prop-mountain":  ("props", "Climbable mountain (Signal Peaks)"),
    "prop-lighthouse":("props", "Lighthouse (Hello Harbor)"),
    # misc
    "boat":           ("misc", "Drifting sailboat"),
    "character":      ("misc", "The player character (shadow + crown kept)"),
}

VALID_EXT = {".glb", ".gltf"}


def load_manifest():
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text())
        except json.JSONDecodeError:
            print(f"warning: {MANIFEST} was corrupt, starting fresh")
    return {"assets": {}}


def save_manifest(m):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n")


def cmd_list():
    m = load_manifest()
    installed = m.get("assets", {})
    width = max(len(s) for s in SLOTS)
    print(f"{'SLOT'.ljust(width)}  STATUS      DESCRIPTION")
    print("-" * (width + 50))
    for slot, (_, desc) in SLOTS.items():
        status = "CUSTOM" if slot in installed else "built-in"
        print(f"{slot.ljust(width)}  {status.ljust(10)}  {desc}")
    if installed:
        print("\ninstalled files:")
        for slot, url in installed.items():
            print(f"  {slot}: {url.split('?')[0]}")


def cmd_remove(slot):
    if slot not in SLOTS:
        sys.exit(f"error: unknown slot '{slot}' (run --list to see slots)")
    m = load_manifest()
    if slot not in m["assets"]:
        print(f"{slot} is already using the built-in model")
        return
    old = m["assets"].pop(slot)
    save_manifest(m)
    # tidy up the copied file too
    old_path = ROOT / old.split("?")[0]
    if old_path.exists():
        old_path.unlink()
    print(f"✓ {slot} reverted to the built-in model — refresh the browser")


def cmd_set(slot, src_arg):
    if slot not in SLOTS:
        sys.exit(f"error: unknown slot '{slot}' (run --list to see slots)")
    src = Path(src_arg).expanduser().resolve()
    if not src.exists():
        sys.exit(f"error: file not found: {src}")
    if src.suffix.lower() not in VALID_EXT:
        sys.exit(f"error: expected a .glb or .gltf file, got '{src.suffix}'\n"
                 f"tip: export from Blender as glTF Binary (.glb) — single file, textures embedded")
    if src.suffix.lower() == ".gltf":
        print("note: .gltf may reference external .bin/texture files; "
              ".glb (single file) is safer. Proceeding anyway.")

    folder, desc = SLOTS[slot]
    dest_dir = ASSETS / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slot}{src.suffix.lower()}"
    shutil.copy2(src, dest)

    m = load_manifest()
    # version query defeats browser caching when you re-export
    rel = dest.relative_to(ROOT).as_posix()
    m["assets"][slot] = f"{rel}?v={int(time.time())}"
    save_manifest(m)

    size_kb = dest.stat().st_size / 1024
    print(f"✓ installed {slot}  ({desc})")
    print(f"  {src}  →  {dest.relative_to(ROOT)}  [{size_kb:.0f} KB]")
    print("  refresh the browser (Cmd+R) to see it in the world")


def main(argv):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return
    if argv[1] == "--list":
        cmd_list()
    elif argv[1] == "--remove":
        if len(argv) != 3:
            sys.exit("usage: set-asset.py --remove <slot>")
        cmd_remove(argv[2])
    else:
        if len(argv) != 3:
            sys.exit("usage: set-asset.py <slot> <path-to-model.glb>   (or --list)")
        cmd_set(argv[1], argv[2])


if __name__ == "__main__":
    main(sys.argv)
