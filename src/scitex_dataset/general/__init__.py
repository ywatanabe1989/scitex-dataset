#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-30 10:00:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/general/__init__.py

"""
General scientific dataset sources.

Platforms:
- zenodo: CERN's general scientific repository
- figshare: Research data sharing (future)
"""

from . import zenodo
from .zenodo import (
    ZENODO_API,
    fetch_all_datasets,
    fetch_datasets,
    format_dataset,
)

__all__ = [
    "zenodo",
    "ZENODO_API",
    "fetch_datasets",
    "fetch_all_datasets",
    "format_dataset",
]

# EOF
