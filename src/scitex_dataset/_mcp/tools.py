#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP tools registration for scitex-dataset.

This module provides a function to register all scitex-dataset MCP tools
with an external FastMCP server (e.g., scitex-python's unified MCP server).
"""

from typing import Any, Dict, List, Optional


def register_all_tools(mcp) -> None:
    """Register all scitex-dataset tools with an MCP server.

    Parameters
    ----------
    mcp : FastMCP
        The FastMCP server instance to register tools with.
    """

    # OpenNeuro
    @mcp.tool()
    def dataset_openneuro_fetch(
        max_datasets: int = 100,
        batch_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """[dataset] Fetch metadata from OpenNeuro (BIDS neuroimaging)."""
        from ..neuroscience.openneuro import fetch_all_datasets, format_dataset

        raw = fetch_all_datasets(
            batch_size=batch_size,
            max_datasets=max_datasets if max_datasets > 0 else None,
        )
        return [format_dataset(ds) for ds in raw]

    # DANDI
    @mcp.tool()
    def dataset_dandi_fetch(max_datasets: int = 100) -> List[Dict[str, Any]]:
        """[dataset] Fetch metadata from DANDI Archive (NWB neurophysiology)."""
        from ..neuroscience.dandi import fetch_all_datasets, format_dataset

        raw = fetch_all_datasets(
            max_datasets=max_datasets if max_datasets > 0 else None
        )
        return [format_dataset(ds) for ds in raw]

    # PhysioNet
    @mcp.tool()
    def dataset_physionet_fetch(max_datasets: int = 100) -> List[Dict[str, Any]]:
        """[dataset] Fetch metadata from PhysioNet (EEG/ECG/physiology)."""
        from ..neuroscience.physionet import fetch_all_datasets, format_dataset

        raw = fetch_all_datasets(
            max_datasets=max_datasets if max_datasets > 0 else None
        )
        return [format_dataset(ds) for ds in raw]

    # Search
    @mcp.tool()
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
        """[dataset] Search and filter datasets by criteria."""
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

    # List sources
    @mcp.tool()
    def dataset_list_sources() -> Dict[str, Any]:
        """[dataset] List available dataset sources."""
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
    @mcp.tool()
    def dataset_db_build(
        sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """[dataset] Build/rebuild the local dataset database."""
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

    @mcp.tool()
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
        """[dataset] Search local database with full-text search."""
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

    @mcp.tool()
    def dataset_db_stats() -> Dict[str, Any]:
        """[dataset] Get local database statistics."""
        from .. import database

        return database.get_stats()


# EOF
