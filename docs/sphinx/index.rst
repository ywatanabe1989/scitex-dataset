.. scitex-dataset documentation master file

scitex-dataset - Neuroscience Dataset Fetcher
==============================================

**scitex-dataset** is a unified Python interface for fetching neuroscience datasets from multiple sources including OpenNeuro, DANDI Archive, and PhysioNet.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   cli_reference
   sources

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/scitex_dataset

Key Features
------------

- **Unified Interface**: Single API for multiple neuroscience data repositories
- **Multiple Sources**: OpenNeuro, DANDI Archive, PhysioNet, and more
- **CLI & Python API**: Use from command line or import as a library
- **BIDS/NWB Support**: Works with standard neuroimaging data formats
- **MCP Integration**: AI agents can fetch datasets via MCP server

Supported Sources
-----------------

- **OpenNeuro**: BIDS-formatted neuroimaging datasets
- **DANDI Archive**: NWB-formatted neurophysiology data
- **PhysioNet**: Physiological signal databases
- **Zenodo**: General scientific datasets

Quick Example
-------------

Python API:

.. code-block:: python

    from scitex_dataset import fetch

    # Fetch from OpenNeuro
    data = fetch("ds000001", source="openneuro")

    # Search across sources
    results = search("EEG epilepsy")

CLI:

.. code-block:: bash

    # Fetch a dataset
    scitex-dataset fetch ds000001 --source openneuro

    # Search for datasets
    scitex-dataset search "fMRI visual"

    # List available sources
    scitex-dataset sources

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
