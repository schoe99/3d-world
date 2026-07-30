#!/bin/zsh
# Install a custom model for: npc-gully
# Usage: ./scripts/set-gully-seagull.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" npc-gully "$@"
