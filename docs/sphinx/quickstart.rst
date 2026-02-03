Quickstart
==========

This guide will help you get started with scitex-dataset quickly.

Basic Usage
-----------

Fetching a Dataset
~~~~~~~~~~~~~~~~~~

Use the CLI to fetch datasets:

.. code-block:: bash

    # Fetch from OpenNeuro
    scitex-dataset fetch ds000001 --source openneuro --output ./data

    # Fetch from DANDI
    scitex-dataset fetch 000003 --source dandi --output ./data

Python API:

.. code-block:: python

    from scitex_dataset import fetch

    # Fetch returns the local path to the dataset
    path = fetch("ds000001", source="openneuro", output="./data")

Searching for Datasets
~~~~~~~~~~~~~~~~~~~~~~

Search across multiple sources:

.. code-block:: bash

    # Search by keyword
    scitex-dataset search "EEG epilepsy"

    # Search specific source
    scitex-dataset search "fMRI" --source openneuro

Python API:

.. code-block:: python

    from scitex_dataset import search

    results = search("EEG epilepsy")
    for result in results:
        print(f"{result['id']}: {result['title']}")

Listing Sources
~~~~~~~~~~~~~~~

View available data sources:

.. code-block:: bash

    scitex-dataset sources

Next Steps
----------

- See :doc:`cli_reference` for full CLI documentation
- See :doc:`api/scitex_dataset` for Python API reference
- See :doc:`sources` for details on each data source
