#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:30:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/neuroscience/__init__.py

"""
Neuroscience dataset sources.

Platforms:
- openneuro: BIDS neuroimaging (MRI, EEG, MEG, iEEG, PET)
- dandi: NWB neurophysiology
- physionet: EEG, ECG, physiological signals
"""

from . import dandi, openneuro, physionet
from .openneuro import (
    OPENNEURO_API,
    fetch_all_datasets,
    fetch_datasets,
    format_dataset,
)

__all__ = [
    # Platforms
    "openneuro",
    "dandi",
    "physionet",
    # Convenience (OpenNeuro as default)
    "OPENNEURO_API",
    "fetch_datasets",
    "fetch_all_datasets",
    "format_dataset",
]

# EOF
