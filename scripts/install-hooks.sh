#!/bin/sh
set -eu
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
echo "Hooks installed."
