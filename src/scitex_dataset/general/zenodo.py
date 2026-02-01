#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-30 10:00:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/general/zenodo.py

"""
Zenodo API client for scientific dataset discovery.

Zenodo is a general-purpose open repository developed under the European
OpenAIRE program and operated by CERN. It allows researchers to deposit
research papers, data sets, research software, reports, and any other
research related digital artifacts.

API Documentation: https://developers.zenodo.org/
"""

from typing import Optional

import httpx

ZENODO_API = "https://zenodo.org/api"


def fetch_datasets(
    query: str = "",
    page: int = 1,
    size: int = 25,  # Unauthenticated limit is 25 with query filters
    sort: str = "mostrecent",
    type_filter: str = "dataset",
) -> dict:
    """
    Fetch datasets from Zenodo.

    Parameters
    ----------
    query : str
        Search query string (Elasticsearch query syntax).
    page : int
        Page number (1-indexed).
    size : int
        Number of results per page (max 10000).
    sort : str
        Sort order: 'bestmatch', 'mostrecent', '-mostrecent'.
    type_filter : str
        Resource type filter: 'dataset', 'software', 'publication', etc.

    Returns
    -------
    dict
        API response with 'hits' containing records.
    """
    # Build query with type filter
    q_parts = []
    if type_filter:
        q_parts.append(f"resource_type.type:{type_filter}")
    if query:
        q_parts.append(f"({query})")

    q_value = " AND ".join(q_parts) if q_parts else ""

    # Build URL manually to avoid over-encoding the query parameter
    # Note: Unauthenticated API limit is 25 for queries with filters
    effective_size = min(size, 25)
    url_parts = [
        f"page={page}",
        f"size={effective_size}",
        f"sort={sort}",
    ]
    if q_value:
        url_parts.append(f"q={q_value}")

    url = f"{ZENODO_API}/records?{'&'.join(url_parts)}"

    response = httpx.get(url, timeout=60)
    response.raise_for_status()
    return response.json()


def fetch_all_datasets(
    query: str = "",
    max_datasets: Optional[int] = None,
    page_size: int = 25,  # Unauthenticated limit is 25 with query filters
    type_filter: str = "dataset",
    logger=None,
) -> list[dict]:
    """
    Fetch all datasets from Zenodo with pagination.

    Parameters
    ----------
    query : str
        Search query string.
    max_datasets : int, optional
        Maximum number of datasets to fetch.
    page_size : int
        Datasets per request.
    type_filter : str
        Resource type filter (default: 'dataset').
    logger : optional
        Logger for progress messages.

    Returns
    -------
    list[dict]
        List of raw record dictionaries.
    """
    all_datasets = []
    page = 1

    while True:
        if logger:
            logger.info(f"Fetching Zenodo page {page}...")

        data = fetch_datasets(
            query=query,
            page=page,
            size=page_size,
            type_filter=type_filter,
        )

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break

        all_datasets.extend(hits)

        if logger:
            logger.info(f"  Retrieved {len(hits)} records (total: {len(all_datasets)})")

        # Check if we've reached max
        if max_datasets and len(all_datasets) >= max_datasets:
            all_datasets = all_datasets[:max_datasets]
            break

        # Check if there are more pages
        total = data.get("hits", {}).get("total", 0)
        if len(all_datasets) >= total:
            break

        page += 1

    return all_datasets


def format_dataset(record: dict) -> dict:
    """
    Format a Zenodo record into a standardized dataset dictionary.

    Parameters
    ----------
    record : dict
        Raw Zenodo record from API.

    Returns
    -------
    dict
        Standardized dataset dictionary.
    """
    metadata = record.get("metadata", {})
    stats = record.get("stats", {})
    files = record.get("files", [])

    # Extract creators/authors
    creators = metadata.get("creators", [])
    authors = [c.get("name", "") for c in creators]

    # Calculate total file size
    total_size = sum(f.get("size", 0) for f in files)

    # Extract keywords/subjects
    keywords = metadata.get("keywords", [])
    subjects = [s.get("term", "") for s in metadata.get("subjects", [])]

    # Get license
    license_info = metadata.get("license", {})
    if isinstance(license_info, dict):
        license_name = license_info.get("id", "")
    else:
        license_name = str(license_info)

    # Get resource type
    resource_type = metadata.get("resource_type", {})
    if isinstance(resource_type, dict):
        dataset_type = resource_type.get("type", "")
        dataset_subtype = resource_type.get("subtype", "")
    else:
        dataset_type = str(resource_type)
        dataset_subtype = ""

    return {
        "id": str(record.get("id", "")),
        "doi": record.get("doi", metadata.get("doi", "")),
        "name": metadata.get("title", ""),
        "description": metadata.get("description", ""),
        "created": record.get("created", ""),
        "modified": record.get("updated", ""),
        "publish_date": metadata.get("publication_date", ""),
        "version": metadata.get("version", ""),
        "authors": authors,
        "keywords": keywords + subjects,
        "license": license_name,
        "dataset_type": dataset_type,
        "dataset_subtype": dataset_subtype,
        "n_files": len(files),
        "size_bytes": total_size,
        "size_gb": round(total_size / (1024**3), 3) if total_size else 0,
        "views": stats.get("views", 0),
        "downloads": stats.get("downloads", 0),
        "url": record.get("links", {}).get(
            "html", f"https://zenodo.org/record/{record.get('id', '')}"
        ),
        "source": "zenodo",
    }


# EOF
