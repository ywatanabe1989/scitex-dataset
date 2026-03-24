---
name: scitex-dataset
description: Dataset fetcher for neuroscience research - OpenNeuro, DANDI, PhysioNet with local database search and BIDS support. Use when finding, downloading, or searching neuroscience datasets.
allowed-tools: mcp__scitex__dataset_*
---

# Dataset Management with scitex-dataset

## Quick Start

```python
from scitex_dataset import search, fetch

# Search datasets across sources
results = search("epilepsy EEG", source="openneuro")

# Fetch dataset
fetch("ds003104", output_dir="./data/")
```

## CLI Commands

```bash
scitex-dataset search "epilepsy EEG" --source openneuro
scitex-dataset fetch ds003104 -o ./data/
scitex-dataset db build          # Build local search database
scitex-dataset db search "motor" # Search local DB
scitex-dataset db stats          # Database statistics
scitex-dataset list-sources      # Available data sources

# MCP & Skills
scitex-dataset mcp start
scitex-dataset skills list
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `dataset_search` | Search datasets across sources |
| `dataset_openneuro_fetch` | Fetch from OpenNeuro |
| `dataset_dandi_fetch` | Fetch from DANDI |
| `dataset_physionet_fetch` | Fetch from PhysioNet |
| `dataset_db_build` | Build local search database |
| `dataset_db_search` | Search local database |
| `dataset_db_stats` | Database statistics |
| `dataset_list_sources` | List available sources |
