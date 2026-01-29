#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:20:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/scripts/fetch_openneuro.py

"""
Fetch dataset metadata from OpenNeuro using scitex session.

Usage:
    python scripts/fetch_openneuro.py --max-datasets 100
"""

import scitex as stx

from scitex_dataset import fetch_all_datasets, format_dataset


@stx.session
def main(
    batch_size: int = 100,
    max_datasets: int = 0,
    logger=stx.session.INJECTED,
):
    """Fetch dataset metadata from OpenNeuro GraphQL API

    Args:
        batch_size: Number of datasets to fetch per request
        max_datasets: Maximum number of datasets to fetch (0 for all)
    """
    if max_datasets == 0:
        max_datasets = None

    logger.info("Fetching datasets from OpenNeuro...")

    try:
        datasets = fetch_all_datasets(
            batch_size=batch_size,
            max_datasets=max_datasets,
            logger=logger,
        )
    except Exception as exc:
        logger.error(f"Failed to fetch datasets: {exc}")
        return 1

    if not datasets:
        logger.warning("No datasets fetched")
        return 1

    formatted = [format_dataset(ds) for ds in datasets]

    for ds in formatted[:10]:
        logger.info(f"{ds['id']}: {ds['name']} ({ds['n_subjects']} subjects)")

    stx.io.save(formatted, "openneuro_datasets.json")
    logger.info(f"Saved {len(formatted)} datasets to openneuro_datasets.json")

    return 0


if __name__ == "__main__":
    main()

# EOF
