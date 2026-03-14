#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/00_run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "Usage: $(basename "$0") [-h]"
    echo ""
    echo "Run all scitex-dataset examples sequentially."
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
}

case "${1:-}" in
-h | --help)
    usage
    exit 0
    ;;
esac

cd "$SCRIPT_DIR"

echo "Running all examples..."
echo

for script in 01_*.py 02_*.py 03_*.sh 04_*.py; do
    if [[ -f "$script" ]]; then
        echo "=== Running $script ==="
        if [[ "$script" == *.py ]]; then
            python "$script"
        else
            bash "$script"
        fi
        echo
    fi
done

echo "All examples completed."

# EOF
