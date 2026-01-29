#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:45:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/_mcp/server.py

"""
MCP server for scitex-dataset - unified scientific dataset discovery.

Usage:
    fastmcp run scitex_dataset._mcp.server:mcp
    # or
    scitex-dataset mcp start
"""

from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from .._branding import get_mcp_instructions, get_mcp_server_name

mcp = FastMCP(
    name=get_mcp_server_name(),
    instructions=get_mcp_instructions(),
)


@mcp.tool
def dataset_openneuro_fetch(
    max_datasets: int = 100,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Fetch dataset metadata from OpenNeuro.

    OpenNeuro hosts BIDS-formatted neuroimaging data including
    MRI, EEG, MEG, iEEG, and PET.

    Parameters
    ----------
    max_datasets : int
        Maximum datasets to fetch (0 for all).
    batch_size : int
        Datasets per API request.

    Returns
    -------
    list
        List of formatted dataset dictionaries with fields:
        id, name, n_subjects, modalities, tasks, size_gb, downloads, readme, etc.
    """
    from ..neuroscience.openneuro import fetch_all_datasets, format_dataset

    raw = fetch_all_datasets(
        batch_size=batch_size,
        max_datasets=max_datasets if max_datasets > 0 else None,
    )
    return [format_dataset(ds) for ds in raw]


@mcp.tool
def dataset_dandi_fetch(max_datasets: int = 100) -> List[Dict[str, Any]]:
    """Fetch dataset metadata from DANDI Archive.

    DANDI hosts neurophysiology data in NWB format.

    Parameters
    ----------
    max_datasets : int
        Maximum datasets to fetch (0 for all).

    Returns
    -------
    list
        List of formatted dandiset dictionaries.
    """
    from ..neuroscience.dandi import fetch_all_datasets, format_dataset

    raw = fetch_all_datasets(max_datasets=max_datasets if max_datasets > 0 else None)
    return [format_dataset(ds) for ds in raw]


@mcp.tool
def dataset_physionet_fetch(max_datasets: int = 100) -> List[Dict[str, Any]]:
    """Fetch dataset metadata from PhysioNet.

    PhysioNet hosts physiological signal databases including
    EEG, ECG, EMG, and other biomedical signals.

    Parameters
    ----------
    max_datasets : int
        Maximum datasets to fetch (0 for all).

    Returns
    -------
    list
        List of formatted database dictionaries.
    """
    from ..neuroscience.physionet import fetch_all_datasets, format_dataset

    raw = fetch_all_datasets(max_datasets=max_datasets if max_datasets > 0 else None)
    return [format_dataset(ds) for ds in raw]


@mcp.tool
def dataset_search(
    datasets: List[Dict[str, Any]],
    modality: Optional[str] = None,
    min_subjects: Optional[int] = None,
    max_subjects: Optional[int] = None,
    task_contains: Optional[str] = None,
    text_query: Optional[str] = None,
    min_downloads: Optional[int] = None,
    has_readme: bool = False,
    sort_by: str = "downloads",
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """Search and filter datasets by criteria.

    Parameters
    ----------
    datasets : list
        List of dataset dictionaries (from fetch tools).
    modality : str, optional
        Filter by modality (mri, eeg, meg, etc.).
    min_subjects : int, optional
        Minimum number of subjects.
    max_subjects : int, optional
        Maximum number of subjects.
    task_contains : str, optional
        Filter by task name substring.
    text_query : str, optional
        Search in name and readme text.
    min_downloads : int, optional
        Minimum download count.
    has_readme : bool
        Only include datasets with readme.
    sort_by : str
        Sort by: downloads, views, n_subjects, size_gb.
    limit : int
        Maximum results to return.

    Returns
    -------
    list
        Filtered and sorted datasets.
    """
    from ..search import search_datasets, sort_datasets

    results = search_datasets(
        datasets,
        modality=modality,
        min_subjects=min_subjects,
        max_subjects=max_subjects,
        task_contains=task_contains,
        text_query=text_query,
        min_downloads=min_downloads,
        has_readme=has_readme,
    )

    results = sort_datasets(results, by=sort_by, descending=True)

    return results[:limit]


@mcp.tool
def dataset_list_sources() -> Dict[str, Any]:
    """List available dataset sources.

    Returns
    -------
    dict
        Dictionary with source names and descriptions.
    """
    return {
        "sources": {
            "openneuro": {
                "name": "OpenNeuro",
                "description": "BIDS neuroimaging (MRI, EEG, MEG, iEEG, PET)",
                "url": "https://openneuro.org",
                "format": "BIDS",
            },
            "dandi": {
                "name": "DANDI Archive",
                "description": "NWB neurophysiology data",
                "url": "https://dandiarchive.org",
                "format": "NWB",
            },
            "physionet": {
                "name": "PhysioNet",
                "description": "EEG, ECG, physiological signals",
                "url": "https://physionet.org",
                "format": "Various",
            },
        },
        "count": 3,
    }


# Database tools
@mcp.tool
def dataset_db_build(
    sources: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build/rebuild the local dataset database.

    Fetches metadata from all sources and indexes them in a local
    SQLite database for fast full-text searching.

    Parameters
    ----------
    sources : list, optional
        Sources to index: ["openneuro", "dandi", "physionet"].
        Default: all sources.

    Returns
    -------
    dict
        Build results with counts per source.
    """
    from .. import database

    counts = database.build(sources=sources)
    stats = database.get_stats()

    return {
        "success": True,
        "indexed": counts,
        "total": sum(counts.values()),
        "database_path": stats.get("path"),
        "size_mb": stats.get("size_mb"),
    }


@mcp.tool
def dataset_db_search(
    query: Optional[str] = None,
    source: Optional[str] = None,
    modality: Optional[str] = None,
    min_subjects: Optional[int] = None,
    max_subjects: Optional[int] = None,
    min_downloads: Optional[int] = None,
    has_readme: bool = False,
    limit: int = 20,
    order_by: str = "downloads",
) -> List[Dict[str, Any]]:
    """Search the local database with full-text search.

    Requires db_build to have been run first.

    Parameters
    ----------
    query : str, optional
        Full-text search query (searches name, readme, tasks).
    source : str, optional
        Filter by source: "openneuro", "dandi", "physionet".
    modality : str, optional
        Filter by modality (e.g., "mri", "eeg").
    min_subjects : int, optional
        Minimum number of subjects.
    max_subjects : int, optional
        Maximum number of subjects.
    min_downloads : int, optional
        Minimum download count.
    has_readme : bool
        Only include datasets with readme.
    limit : int
        Maximum results (default: 20).
    order_by : str
        Order by: downloads, views, n_subjects, size_gb, name.

    Returns
    -------
    list
        List of matching datasets.
    """
    from .. import database

    return database.search(
        query=query,
        source=source,
        modality=modality,
        min_subjects=min_subjects,
        max_subjects=max_subjects,
        min_downloads=min_downloads,
        has_readme=has_readme,
        limit=limit,
        order_by=order_by,
    )


@mcp.tool
def dataset_db_stats() -> Dict[str, Any]:
    """Get local database statistics.

    Returns
    -------
    dict
        Statistics including counts per source, last build time, etc.
    """
    from .. import database

    return database.get_stats()


@mcp.resource("scitex-dataset://readme")
def get_readme() -> str:
    """Get package README."""
    from pathlib import Path

    readme_path = Path(__file__).parent.parent.parent.parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text()
    return "scitex-dataset: Unified interface for scientific dataset discovery."


if __name__ == "__main__":
    mcp.run()

# EOF
