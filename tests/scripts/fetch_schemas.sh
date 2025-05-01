#!/usr/bin/env bash
set -e

# Determine project root relative to this script
eval "SCRIPT_DIR=$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)"
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Output directory for schema files
OUTPUT_DIR="$PROJECT_ROOT/tests/input/schemas"

echo "Fetching latest gnomAD schema..."
python -m gnomad.schema fetch --output-dir "$OUTPUT_DIR"
echo "Schema and log saved to $OUTPUT_DIR" 