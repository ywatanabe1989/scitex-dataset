CLI Reference
=============

The ``scitex-dataset`` command-line interface provides easy access to dataset operations.

Global Options
--------------

.. code-block:: bash

    scitex-dataset --help
    scitex-dataset --version

Commands
--------

fetch
~~~~~

Fetch a dataset from a specified source.

.. code-block:: bash

    scitex-dataset fetch DATASET_ID [OPTIONS]

Options:

- ``--source, -s``: Data source (openneuro, dandi, physionet, zenodo)
- ``--output, -o``: Output directory (default: current directory)
- ``--include``: Include file patterns
- ``--exclude``: Exclude file patterns

Examples:

.. code-block:: bash

    # Fetch OpenNeuro dataset
    scitex-dataset fetch ds000001 --source openneuro

    # Fetch to specific directory
    scitex-dataset fetch ds000001 -s openneuro -o ./datasets

    # Fetch only specific files
    scitex-dataset fetch ds000001 -s openneuro --include "*.nii.gz"

search
~~~~~~

Search for datasets across sources.

.. code-block:: bash

    scitex-dataset search QUERY [OPTIONS]

Options:

- ``--source, -s``: Limit search to specific source
- ``--limit, -n``: Maximum number of results

Examples:

.. code-block:: bash

    # Search all sources
    scitex-dataset search "EEG epilepsy"

    # Search specific source
    scitex-dataset search "fMRI visual" --source openneuro

    # Limit results
    scitex-dataset search "MEG" --limit 10

sources
~~~~~~~

List available data sources.

.. code-block:: bash

    scitex-dataset sources

Output shows each source with its description and status.

info
~~~~

Get information about a specific dataset.

.. code-block:: bash

    scitex-dataset info DATASET_ID --source SOURCE

Examples:

.. code-block:: bash

    scitex-dataset info ds000001 --source openneuro
