#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/01_fetch_openneuro.py

"""
Example: Fetch datasets from OpenNeuro

This example demonstrates how to fetch dataset metadata from OpenNeuro
and save it to a JSON file.
"""

import json
from pathlib import Path

from scitex_dataset import fetch_all_datasets, format_dataset

OUTPUT_DIR = Path(__file__).parent / "01_fetch_openneuro_out"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Fetching datasets from OpenNeuro...")
    raw_datasets = fetch_all_datasets(max_datasets=20)

    print(f"Formatting {len(raw_datasets)} datasets...")
    datasets = [format_dataset(d) for d in raw_datasets]

    print("\nFirst 5 datasets:")
    for ds in datasets[:5]:
        print(f"  {ds['id']}: {ds['name']}")
        print(f"    Subjects: {ds['n_subjects']}, Modality: {ds['primary_modality']}")
        print(f"    Downloads: {ds['downloads']}")

    output_path = OUTPUT_DIR / "openneuro_datasets.json"
    with open(output_path, "w") as f:
        json.dump(datasets, f, indent=2)
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()

# EOF
