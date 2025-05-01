#!/usr/bin/env bash
set -e

# Determine project root relative to this script
eval "SCRIPT_DIR=$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)"
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Input and output paths
INPUT_SCHEMA="$PROJECT_ROOT/tests/input/schemas/gnomad_schema.json"
OUTPUT_DIR="$PROJECT_ROOT/tests/input/analyzed_schemas"
OUTPUT_FILE="$OUTPUT_DIR/query_field_map.json"

mkdir -p "$OUTPUT_DIR"

# Analyze schema and save query field map
python -m gnomad.schema analyze --schema "$INPUT_SCHEMA" --output "$OUTPUT_FILE"
echo "Analysis result saved to $OUTPUT_FILE" 