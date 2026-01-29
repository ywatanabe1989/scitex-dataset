#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/03_cli_usage.sh

# Example: CLI usage for scitex-dataset

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/03_cli_usage_out"

mkdir -p "$OUTPUT_DIR"

echo "=== CLI Help ==="
scitex-dataset --help

echo
echo "=== OpenNeuro Help ==="
scitex-dataset openneuro --help

echo
echo "=== Fetching 10 datasets ==="
scitex-dataset openneuro -n 10 -o "$OUTPUT_DIR/datasets.json" -v

echo
echo "Output saved to $OUTPUT_DIR/datasets.json"

# EOF
