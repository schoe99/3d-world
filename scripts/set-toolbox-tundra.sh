#!/bin/zsh
# Install a custom model for: island-skills
# Usage: ./scripts/set-toolbox-tundra.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" island-skills "$@"
