#!/bin/zsh
# Install a custom model for: island-signal
# Usage: ./scripts/set-signal-peaks.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" island-signal "$@"
