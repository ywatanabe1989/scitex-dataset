# SciTeX Dataset

Dataset fetcher for neuroscience research.

## Installation

```bash
pip install scitex-dataset
```

## Usage

### Python API

```python
from scitex_dataset import fetch_all_datasets, format_dataset

# Fetch first 10 datasets
datasets = fetch_all_datasets(max_datasets=10)

# Format for analysis
formatted = [format_dataset(ds) for ds in datasets]

for ds in formatted:
    print(f"{ds['id']}: {ds['name']} ({ds['n_subjects']} subjects)")
```

### CLI

```bash
# Fetch and save to JSON
scitex-dataset openneuro -n 100 -o datasets.json -v

# Fetch all datasets
scitex-dataset openneuro -o all_datasets.json
```

### With SciTeX Session

```python
import scitex as stx
from scitex_dataset import fetch_all_datasets, format_dataset

@stx.session
def main(logger=stx.session.INJECTED):
    datasets = fetch_all_datasets(max_datasets=100, logger=logger)
    formatted = [format_dataset(ds) for ds in datasets]
    stx.io.save(formatted, "openneuro_datasets.json")
    return 0

if __name__ == "__main__":
    main()
```

## Data Sources

- **OpenNeuro**: Free and open platform for sharing neuroimaging data
  - BIDS-formatted datasets
  - MRI, EEG, MEG, iEEG, PET data

## License

AGPL-3.0
