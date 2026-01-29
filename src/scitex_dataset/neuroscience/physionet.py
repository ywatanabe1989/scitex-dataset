#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:40:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/neuroscience/physionet.py

"""
PhysioNet dataset fetcher.

PhysioNet hosts physiological signal databases including EEG, ECG, EMG,
and other biomedical signals.

API: https://physionet.org/api/v1/

Example:
    >>> from scitex_dataset.neuroscience import physionet
    >>> datasets = physionet.fetch_all_datasets(max_datasets=10)
    >>> formatted = [physionet.format_dataset(ds) for ds in datasets]
"""

from __future__ import annotations

from typing import Optional

import httpx as _httpx

PHYSIONET_API = "https://physionet.org"

__all__ = [
    "PHYSIONET_API",
    "fetch_datasets",
    "fetch_all_datasets",
    "format_dataset",
]


def fetch_datasets(page: int = 1) -> dict:
    """Fetch a single page of databases from PhysioNet."""
    response = _httpx.get(
        f"{PHYSIONET_API}/rest/database-list/",
        params={"page": page},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def fetch_all_datasets(
    max_datasets: Optional[int] = None,
    logger=None,
) -> list[dict]:
    """Fetch all databases from PhysioNet with pagination."""
    all_datasets = []
    page = 1

    while True:
        try:
            result = fetch_datasets(page=page)
        except _httpx.HTTPStatusError as exc:
            if logger:
                logger.error(f"HTTP Error: {exc}")
            break
        except _httpx.RequestError as exc:
            if logger:
                logger.error(f"Request Error: {exc}")
            break

        # PhysioNet returns a list directly or paginated dict
        if isinstance(result, list):
            databases = result
            has_next = False
        else:
            databases = result.get("results", result.get("databases", []))
            has_next = bool(result.get("next"))

        if not databases:
            break

        all_datasets.extend(databases)

        if logger:
            logger.info(f"Fetched {len(all_datasets)} databases...")

        if max_datasets and len(all_datasets) >= max_datasets:
            all_datasets = all_datasets[:max_datasets]
            break

        if not has_next:
            break

        page += 1

    return all_datasets


def format_dataset(database: dict) -> dict:
    """Extract and format PhysioNet database information."""
    # Handle different response formats
    slug = database.get("slug", database.get("short_name", ""))
    title = database.get("title", database.get("name", "N/A"))

    return {
        "id": slug,
        "name": title,
        "version": database.get("version", ""),
        "abstract": database.get("abstract", database.get("description", "")),
        "doi": database.get("doi", ""),
        "license": database.get("license", {}).get("name", "")
        if isinstance(database.get("license"), dict)
        else database.get("license", ""),
        "n_subjects": database.get("subject_count", 0),
        "n_records": database.get("record_count", 0),
        "size_gb": round((database.get("total_size") or 0) / (1024**3), 2),
        "publish_date": database.get("publish_date", ""),
        "url": f"https://physionet.org/content/{slug}/" if slug else "",
        # PhysioNet-specific
        "data_access": database.get("data_access", ""),
    }


# EOF
