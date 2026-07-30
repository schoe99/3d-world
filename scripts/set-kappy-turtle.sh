#!/bin/zsh
# Install a custom model for: npc-kappy
# Usage: ./scripts/set-kappy-turtle.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" npc-kappy "$@"
