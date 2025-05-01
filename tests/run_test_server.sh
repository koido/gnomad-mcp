#!/usr/bin/env bash
set -euo pipefail

# Always run test_server.py from the tests directory, regardless of where the script is called from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧪 Running gnomAD MCP server tests"

# Set PYTHONPATH to parent directory so 'server' can be imported
PYTHONPATH=.. pytest -q test_server.py 