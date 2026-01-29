#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:40:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/neuroscience/dandi.py

"""
DANDI Archive dataset fetcher.

DANDI (Distributed Archives for Neurophysiology Data Integration) hosts
neurophysiology data in NWB (Neurodata Without Borders) format.

API: https://api.dandiarchive.org/api

Example:
    >>> from scitex_dataset.neuroscience import dandi
    >>> datasets = dandi.fetch_all_datasets(max_datasets=10)
    >>> formatted = [dandi.format_dataset(ds) for ds in datasets]
"""

from __future__ import annotations

from typing import Optional

import httpx as _httpx

DANDI_API = "https://api.dandiarchive.org/api"

__all__ = [
    "DANDI_API",
    "fetch_datasets",
    "fetch_all_datasets",
    "format_dataset",
]


def fetch_datasets(
    page: int = 1,
    page_size: int = 100,
    ordering: str = "-modified",
) -> dict:
    """Fetch a single page of dandisets from DANDI Archive."""
    response = _httpx.get(
        f"{DANDI_API}/dandisets/",
        params={
            "page": page,
            "page_size": page_size,
            "ordering": ordering,
            "draft": "true",
            "empty": "false",
        },
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def fetch_all_datasets(
    max_datasets: Optional[int] = None,
    page_size: int = 100,
    logger=None,
) -> list[dict]:
    """Fetch all dandisets from DANDI Archive with pagination."""
    all_datasets = []
    page = 1

    while True:
        try:
            result = fetch_datasets(page=page, page_size=page_size)
        except _httpx.HTTPStatusError as exc:
            if logger:
                logger.error(f"HTTP Error: {exc}")
            break
        except _httpx.RequestError as exc:
            if logger:
                logger.error(f"Request Error: {exc}")
            break

        results = result.get("results", [])
        if not results:
            break

        all_datasets.extend(results)

        if logger:
            logger.info(f"Fetched {len(all_datasets)} dandisets...")

        if max_datasets and len(all_datasets) >= max_datasets:
            all_datasets = all_datasets[:max_datasets]
            break

        if not result.get("next"):
            break

        page += 1

    return all_datasets


def format_dataset(dandiset: dict) -> dict:
    """Extract and format dandiset information."""
    draft = dandiset.get("draft_version") or {}
    contact = dandiset.get("contact_person") or ""

    return {
        "id": dandiset.get("identifier", ""),
        "name": draft.get("name", dandiset.get("identifier", "N/A")),
        "created": dandiset.get("created"),
        "modified": dandiset.get("modified"),
        "version": draft.get("version"),
        "status": draft.get("status"),
        "contact": contact,
        "n_assets": draft.get("asset_count", 0),
        "size_bytes": draft.get("size", 0),
        "size_gb": round((draft.get("size") or 0) / (1024**3), 2),
        "url": f"https://dandiarchive.org/dandiset/{dandiset.get('identifier')}",
        # DANDI-specific
        "embargo_status": dandiset.get("embargo_status"),
    }


# EOF
