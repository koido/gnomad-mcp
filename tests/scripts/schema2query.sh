#!/usr/bin/env bash
set -e

# Determine project root relative to this script
eval "SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Input and output paths
INPUT_PATH="$PROJECT_ROOT/tests/input/analyzed_schemas/query_field_map.json"
OUTPUT_DIR="$PROJECT_ROOT/tests/input/schema2query"

mkdir -p "$OUTPUT_DIR"

# Generate GraphQL queries from analyzed schema
python -m gnomad.schema2query --input "$INPUT_PATH" --output-dir "$OUTPUT_DIR"
echo "GraphQL queries and log have been generated in $OUTPUT_DIR" 