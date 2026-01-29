#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:35:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/neuroscience/openneuro.py

"""
OpenNeuro dataset fetcher using GraphQL API.

Example:
    >>> from scitex_dataset import fetch_all_datasets, format_dataset
    >>> datasets = fetch_all_datasets(max_datasets=10)
    >>> formatted = [format_dataset(ds) for ds in datasets]
"""

from __future__ import annotations

from typing import Optional

import httpx as _httpx  # noqa: N812

OPENNEURO_API = "https://openneuro.org/crn/graphql"

__all__ = [
    "OPENNEURO_API",
    "fetch_datasets",
    "fetch_all_datasets",
    "format_dataset",
]


def _make_query(first: int = 10, after: Optional[str] = None) -> str:
    after_arg = f', after: "{after}"' if after else ""
    return f"""
query {{
  datasets(first: {first}{after_arg}) {{
    edges {{
      node {{
        id
        name
        created
        public
        publishDate
        analytics {{ views downloads }}
        draft {{
          modified
          readme
          description {{
            Name BIDSVersion License Authors SeniorAuthor
            DatasetDOI DatasetType Acknowledgements
            HowToAcknowledge Funding ReferencesAndLinks EthicsApprovals
          }}
          summary {{
            modalities primaryModality secondaryModalities
            sessions subjects tasks size totalFiles dataProcessed
          }}
        }}
      }}
    }}
    pageInfo {{ hasNextPage endCursor }}
  }}
}}
"""


def fetch_datasets(first: int = 10, after: Optional[str] = None) -> dict:
    """Fetch a single page of datasets from OpenNeuro."""
    response = _httpx.post(
        OPENNEURO_API,
        json={"query": _make_query(first, after)},
        headers={"Content-Type": "application/json"},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def fetch_all_datasets(
    batch_size: int = 100,
    max_datasets: Optional[int] = None,
    logger=None,
) -> list[dict]:
    """Fetch all datasets from OpenNeuro with pagination."""
    all_datasets = []
    cursor = None

    while True:
        try:
            result = fetch_datasets(first=batch_size, after=cursor)
        except _httpx.HTTPStatusError as exc:
            if logger:
                logger.error(f"HTTP Error: {exc}")
            break
        except _httpx.RequestError as exc:
            if logger:
                logger.error(f"Request Error: {exc}")
            break

        if "errors" in result:
            if logger:
                logger.error(f"GraphQL Errors: {result['errors']}")
            break

        datasets = result.get("data", {}).get("datasets", {})
        edges = datasets.get("edges", [])
        page_info = datasets.get("pageInfo", {})

        for edge in edges:
            all_datasets.append(edge["node"])

        if logger:
            logger.info(f"Fetched {len(all_datasets)} datasets...")

        if max_datasets and len(all_datasets) >= max_datasets:
            break

        if not page_info.get("hasNextPage"):
            break

        cursor = page_info.get("endCursor")

    return all_datasets


def format_dataset(node: dict) -> dict:
    """Extract and format dataset information from raw GraphQL response."""
    draft = node.get("draft") or {}
    description = draft.get("description") or {}
    summary = draft.get("summary") or {}
    analytics = node.get("analytics") or {}

    size_bytes = summary.get("size") or 0
    size_gb = size_bytes / (1024**3)

    return {
        "id": node["id"],
        "name": node.get("name") or description.get("Name", "N/A"),
        "created": node.get("created"),
        "modified": draft.get("modified"),
        "publish_date": node.get("publishDate"),
        "public": node.get("public"),
        "views": analytics.get("views"),
        "downloads": analytics.get("downloads"),
        "readme": draft.get("readme"),
        "bids_version": description.get("BIDSVersion"),
        "license": description.get("License"),
        "authors": description.get("Authors"),
        "senior_author": description.get("SeniorAuthor"),
        "doi": description.get("DatasetDOI"),
        "dataset_type": description.get("DatasetType"),
        "acknowledgements": description.get("Acknowledgements"),
        "how_to_acknowledge": description.get("HowToAcknowledge"),
        "funding": description.get("Funding"),
        "references_and_links": description.get("ReferencesAndLinks"),
        "ethics_approvals": description.get("EthicsApprovals"),
        "modalities": summary.get("modalities", []),
        "primary_modality": summary.get("primaryModality"),
        "secondary_modalities": summary.get("secondaryModalities", []),
        "sessions": summary.get("sessions", []),
        "n_subjects": len(summary.get("subjects") or []),
        "tasks": summary.get("tasks", []),
        "size_gb": round(size_gb, 2),
        "total_files": summary.get("totalFiles", 0),
        "data_processed": summary.get("dataProcessed"),
    }


def _log_dataset(dataset: dict, logger) -> None:
    """Log formatted dataset information (internal use)."""
    logger.info(f"ID: {dataset['id']}")
    logger.info(f"  Name: {dataset['name']}")
    logger.info(f"  Modalities: {dataset['modalities']}")
    logger.info(f"  Subjects: {dataset['n_subjects']}")
    logger.info(f"  Size: {dataset['size_gb']:.2f} GB")


# EOF
