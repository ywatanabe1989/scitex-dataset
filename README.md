# SciTeX Dataset

**Unified access to neuroscience datasets for AI-powered research**

[![PyPI version](https://badge.fury.io/py/scitex-dataset.svg)](https://badge.fury.io/py/scitex-dataset)
[![Tests](https://github.com/ywatanabe1989/scitex-dataset/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-dataset/actions/workflows/test.yml)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

SciTeX Dataset provides a unified interface to discover and fetch metadata from major neuroscience data repositories.

Part of [**SciTeX**](https://scitex.ai).

## Data Sources

| Repository | Description | Data Types |
|------------|-------------|------------|
| **OpenNeuro** | Open platform for sharing neuroimaging data | MRI, EEG, MEG, iEEG, PET |
| **DANDI** | BRAIN Initiative data archive | Electrophysiology, Ophys |
| **PhysioNet** | Physiological signal databases | ECG, EEG, clinical data |

## Quick Start

```bash
pip install scitex-dataset
```

### Python API

```python
from scitex_dataset import fetch_all_datasets, format_dataset

# Fetch datasets from OpenNeuro
datasets = fetch_all_datasets(max_datasets=10)

# Format for analysis
for ds in datasets:
    formatted = format_dataset(ds)
    print(f"{formatted['id']}: {formatted['name']} ({formatted['n_subjects']} subjects)")
```

### CLI

```bash
# Fetch OpenNeuro datasets
scitex-dataset openneuro -n 100 -o datasets.json -v

# Search across repositories
scitex-dataset search "epilepsy EEG" --source openneuro

# Database operations
scitex-dataset db init
scitex-dataset db sync openneuro
scitex-dataset db query "modality:eeg"
```

### MCP Server

SciTeX Dataset includes an **MCP (Model Context Protocol) server**, enabling AI agents like Claude to discover and query neuroscience datasets.

```bash
# Add to Claude Code MCP config
scitex-dataset mcp install

# Or run directly
scitex-dataset mcp start
```

**Available MCP Tools:**

| Tool | Description |
|------|-------------|
| `dataset_openneuro_fetch` | Fetch datasets from OpenNeuro |
| `dataset_openneuro_search` | Search OpenNeuro by query |
| `dataset_dandi_fetch` | Fetch datasets from DANDI Archive |
| `dataset_dandi_search` | Search DANDI by query |
| `dataset_physionet_fetch` | Fetch datasets from PhysioNet |
| `dataset_physionet_search` | Search PhysioNet by query |
| `dataset_search` | Unified search across all repositories |
| `dataset_stats` | Get repository statistics |

### With SciTeX Session

```python
import scitex as stx
from scitex_dataset import fetch_all_datasets, format_dataset

@stx.session
def main(logger=stx.INJECTED):
    datasets = fetch_all_datasets(max_datasets=100, logger=logger)
    formatted = [format_dataset(ds) for ds in datasets]
    stx.io.save(formatted, "openneuro_datasets.json")
    return 0

if __name__ == "__main__":
    main()
```

## Why SciTeX Dataset?

- **Unified Interface**: One API for OpenNeuro, DANDI, PhysioNet, and more
- **AI-Ready**: MCP server enables LLMs to discover relevant datasets
- **Metadata Focus**: Fast metadata queries without downloading full datasets
- **SciTeX Integration**: Works seamlessly with `@stx.session` for reproducible research

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="https://raw.githubusercontent.com/ywatanabe1989/scitex-python/main/docs/assets/images/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
  <br>
  AGPL-3.0 · ywatanabe@scitex.ai
</p>

<!-- EOF -->
