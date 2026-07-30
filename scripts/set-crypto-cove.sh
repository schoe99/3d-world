#!/bin/zsh
# Install a custom model for: island-crypto
# Usage: ./scripts/set-crypto-cove.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" island-crypto "$@"
