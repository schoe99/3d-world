#!/bin/zsh
# Install a custom model for: island-contact
# Usage: ./scripts/set-hello-harbor.sh <path-to-model.glb>
exec python3 "$(dirname "$0")/../set-asset.py" island-contact "$@"
