#!/bin/zsh
# Install a custom model for: character
# Usage: ./scripts/set-character.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" character "$@"
