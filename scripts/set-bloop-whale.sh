#!/bin/zsh
# Install a custom model for: npc-bloop
# Usage: ./scripts/set-bloop-whale.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" npc-bloop "$@"
