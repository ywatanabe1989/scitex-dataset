#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/02_search_datasets.py

"""
Example: Search and filter datasets

This example demonstrates how to search and filter datasets
using various criteria.
"""

import json
from pathlib import Path

from scitex_dataset import (
    fetch_all_datasets,
    format_dataset,
    search_datasets,
    sort_datasets,
)

OUTPUT_DIR = Path(__file__).parent / "02_search_datasets_out"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Fetching datasets from OpenNeuro...")
    raw_datasets = fetch_all_datasets(max_datasets=100)
    datasets = [format_dataset(d) for d in raw_datasets]
    print(f"Total: {len(datasets)} datasets\n")

    # Search by modality
    mri_datasets = search_datasets(datasets, modality="mri")
    print(f"MRI datasets: {len(mri_datasets)}")

    # Search with multiple criteria
    large_mri = search_datasets(
        datasets,
        modality="mri",
        min_subjects=20,
        has_readme=True,
    )
    print(f"MRI with 20+ subjects and readme: {len(large_mri)}")

    # Text search
    memory_datasets = search_datasets(datasets, text_query="memory")
    print(f"Datasets mentioning 'memory': {len(memory_datasets)}")

    # Sort by popularity
    popular = sort_datasets(datasets, by="downloads", descending=True)[:10]
    print("\nTop 10 most downloaded:")
    for ds in popular:
        print(f"  {ds['id']}: {ds['downloads']} downloads - {ds['name']}")

    # Save results
    output_path = OUTPUT_DIR / "mri_large_datasets.json"
    with open(output_path, "w") as f:
        json.dump(large_mri, f, indent=2)
    print(f"\nSaved large MRI datasets to {output_path}")


if __name__ == "__main__":
    main()

# EOF
