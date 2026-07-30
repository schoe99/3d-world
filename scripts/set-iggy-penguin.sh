#!/bin/zsh
# Install a custom model for: npc-iggy
# Usage: ./scripts/set-iggy-penguin.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" npc-iggy "$@"
