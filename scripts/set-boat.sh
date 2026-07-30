#!/bin/zsh
# Install a custom model for: boat
# Usage: ./scripts/set-boat.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" boat "$@"
