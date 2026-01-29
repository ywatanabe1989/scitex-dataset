#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/00_run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Running all examples..."
echo

for script in 01_*.py 02_*.py 03_*.py; do
    if [[ -f "$script" ]]; then
        echo "=== Running $script ==="
        python "$script"
        echo
    fi
done

echo "All examples completed."

# EOF
