#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:27:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/search.py

"""
Unified search interface for neuroscience datasets.

Currently supports:
- OpenNeuro (BIDS neuroimaging)

Future sources:
- DANDI (NWB neurophysiology)
- PhysioNet (EEG/ECG/physiology)
- Zenodo (general scientific)
"""

from __future__ import annotations

from typing import Optional


def search_datasets(
    datasets: list[dict],
    modality: Optional[str] = None,
    min_subjects: Optional[int] = None,
    max_subjects: Optional[int] = None,
    task_contains: Optional[str] = None,
    text_query: Optional[str] = None,
    min_downloads: Optional[int] = None,
    has_readme: bool = False,
) -> list[dict]:
    """Filter datasets by various criteria.

    Args:
        datasets: List of formatted dataset dictionaries
        modality: Filter by modality (e.g., "mri", "eeg", "meg")
        min_subjects: Minimum number of subjects
        max_subjects: Maximum number of subjects
        task_contains: Filter by task name substring
        text_query: Search in name and readme text
        min_downloads: Minimum download count
        has_readme: Only include datasets with readme

    Returns:
        Filtered list of datasets

    Example:
        >>> from scitex_dataset import fetch_all_datasets, format_dataset
        >>> from scitex_dataset.search import search_datasets
        >>> raw = fetch_all_datasets(max_datasets=100)
        >>> datasets = [format_dataset(d) for d in raw]
        >>> eeg_data = search_datasets(datasets, modality="eeg", min_subjects=20)
    """
    results = datasets

    if modality:
        modality_lower = modality.lower()
        results = [
            d
            for d in results
            if modality_lower in [m.lower() for m in (d.get("modalities") or [])]
            or modality_lower == (d.get("primary_modality") or "").lower()
        ]

    if min_subjects is not None:
        results = [d for d in results if d.get("n_subjects", 0) >= min_subjects]

    if max_subjects is not None:
        results = [d for d in results if d.get("n_subjects", 0) <= max_subjects]

    if task_contains:
        task_lower = task_contains.lower()
        results = [
            d
            for d in results
            if any(task_lower in t.lower() for t in (d.get("tasks") or []))
        ]

    if text_query:
        query = text_query.lower()
        results = [
            d
            for d in results
            if query in (d.get("name") or "").lower()
            or query in (d.get("readme") or "").lower()
        ]

    if min_downloads is not None:
        results = [d for d in results if (d.get("downloads") or 0) >= min_downloads]

    if has_readme:
        results = [d for d in results if d.get("readme")]

    return results


def sort_datasets(
    datasets: list[dict],
    by: str = "downloads",
    descending: bool = True,
) -> list[dict]:
    """Sort datasets by a field.

    Args:
        datasets: List of formatted dataset dictionaries
        by: Field to sort by (downloads, views, n_subjects, size_gb, created)
        descending: Sort in descending order

    Returns:
        Sorted list of datasets
    """

    def get_key(d: dict):
        val = d.get(by)
        if val is None:
            return 0 if descending else float("inf")
        return val

    return sorted(datasets, key=get_key, reverse=descending)


# EOF
