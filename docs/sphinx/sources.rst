Data Sources
============

scitex-dataset supports multiple neuroscience data repositories.

OpenNeuro
---------

`OpenNeuro <https://openneuro.org>`_ is a free and open platform for sharing MRI, MEG, EEG, iEEG, and other neuroimaging data.

**Format**: BIDS (Brain Imaging Data Structure)

**Data Types**:

- MRI (structural, functional, diffusion)
- MEG
- EEG
- iEEG
- PET

**Usage**:

.. code-block:: bash

    scitex-dataset fetch ds000001 --source openneuro

.. code-block:: python

    from scitex_dataset import fetch
    fetch("ds000001", source="openneuro")

DANDI Archive
-------------

`DANDI <https://dandiarchive.org>`_ is a platform for publishing and sharing neurophysiology data.

**Format**: NWB (Neurodata Without Borders)

**Data Types**:

- Electrophysiology
- Calcium imaging
- Behavioral data
- Optogenetics

**Usage**:

.. code-block:: bash

    scitex-dataset fetch 000003 --source dandi

.. code-block:: python

    from scitex_dataset import fetch
    fetch("000003", source="dandi")

PhysioNet
---------

`PhysioNet <https://physionet.org>`_ provides open access to large collections of physiological and clinical data.

**Data Types**:

- ECG/EKG
- EEG
- Blood pressure
- Respiration

**Usage**:

.. code-block:: bash

    scitex-dataset fetch mimic3wdb --source physionet

.. code-block:: python

    from scitex_dataset import fetch
    fetch("mimic3wdb", source="physionet")

Zenodo
------

`Zenodo <https://zenodo.org>`_ is a general-purpose open repository for research data.

**Data Types**: Various (filter by neuroscience community)

**Usage**:

.. code-block:: bash

    scitex-dataset fetch 1234567 --source zenodo

.. code-block:: python

    from scitex_dataset import fetch
    fetch("1234567", source="zenodo")
