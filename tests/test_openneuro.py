#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:20:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/tests/test_openneuro.py

"""Tests for OpenNeuro dataset fetcher."""


from scitex_dataset import OPENNEURO_API, fetch_datasets, format_dataset


def test_openneuro_api_url():
    """Test that API URL is correct."""
    assert OPENNEURO_API == "https://openneuro.org/crn/graphql"


def test_fetch_datasets():
    """Test fetching a small number of datasets."""
    result = fetch_datasets(first=2)

    assert "data" in result
    assert "datasets" in result["data"]
    edges = result["data"]["datasets"]["edges"]
    assert len(edges) == 2


def test_format_dataset():
    """Test formatting a dataset node."""
    node = {
        "id": "ds000001",
        "name": "Test Dataset",
        "created": "2020-01-01T00:00:00Z",
        "public": True,
        "publishDate": "2020-01-01T00:00:00Z",
        "analytics": {"views": 100, "downloads": 50},
        "draft": {
            "modified": "2020-06-01T00:00:00Z",
            "readme": "Test README content",
            "description": {
                "Name": "Test Dataset",
                "BIDSVersion": "1.6.0",
                "License": "CC0",
                "Authors": ["Author One", "Author Two"],
            },
            "summary": {
                "modalities": ["mri"],
                "primaryModality": "mri",
                "subjects": ["sub-01", "sub-02", "sub-03"],
                "tasks": ["rest"],
                "size": 1073741824,  # 1 GB
                "totalFiles": 100,
            },
        },
    }

    formatted = format_dataset(node)

    assert formatted["id"] == "ds000001"
    assert formatted["name"] == "Test Dataset"
    assert formatted["n_subjects"] == 3
    assert formatted["size_gb"] == 1.0
    assert formatted["views"] == 100
    assert formatted["downloads"] == 50


def test_format_dataset_missing_fields():
    """Test formatting with missing optional fields."""
    node = {
        "id": "ds000002",
        "name": None,
        "draft": None,
    }

    formatted = format_dataset(node)

    assert formatted["id"] == "ds000002"
    assert formatted["name"] == "N/A"
    assert formatted["n_subjects"] == 0
    assert formatted["size_gb"] == 0.0


# EOF
