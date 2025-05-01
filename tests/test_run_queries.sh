#!/bin/bash

set -euo pipefail

# Check version argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <VERSION>"
  exit 1
fi

VERSION="$1"

OUTPUT_ROOT="./tests/output"
OUTPUT_DIR="${OUTPUT_ROOT}/${VERSION}"

# Clean previous outputs
rm -f ${OUTPUT_DIR}/*
mkdir -p ${OUTPUT_DIR}

echo "Running query runner for version $VERSION..."
python -m gnomad.query --version "$VERSION" --output-root "$OUTPUT_ROOT"