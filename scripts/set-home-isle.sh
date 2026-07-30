#!/bin/zsh
# Install a custom model for: island-home
# Usage: ./scripts/set-home-isle.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" island-home "$@"
