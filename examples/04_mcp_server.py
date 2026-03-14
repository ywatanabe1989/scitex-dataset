#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-03-14 09:00:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/examples/04_mcp_server.py

"""
Example: MCP server tools for AI-agent integration

This example demonstrates the MCP tools available in scitex-dataset,
which AI agents can invoke via the Model Context Protocol.

Note: These tools are the same ones exposed by `scitex-dataset mcp start`.
      Here we call them directly as Python functions for demonstration.
"""

import json
from pathlib import Path

from scitex_dataset._mcp.server import (
    dataset_list_sources,
    dataset_openneuro_fetch,
)

OUTPUT_DIR = Path(__file__).parent / "04_mcp_server_out"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. List available sources (same as MCP tool: dataset_list_sources)
    print("=== MCP Tool: dataset_list_sources ===")
    sources = dataset_list_sources()
    for key, info in sources["sources"].items():
        print(f"  {key}: {info['description']} ({info['domain']})")
    print(f"  Total sources: {sources['count']}")

    # 2. Fetch datasets (same as MCP tool: dataset_openneuro_fetch)
    print("\n=== MCP Tool: dataset_openneuro_fetch ===")
    datasets = dataset_openneuro_fetch(max_datasets=5, batch_size=5)
    print(f"  Fetched {len(datasets)} datasets")
    for ds in datasets:
        print(f"  {ds['id']}: {ds['name'][:60]}")

    # Save results
    output_path = OUTPUT_DIR / "mcp_demo_output.json"
    with open(output_path, "w") as f:
        json.dump({"sources": sources, "sample_datasets": datasets}, f, indent=2)
    print(f"\nSaved to {output_path}")

    # 3. Show how to start the MCP server
    print("\n=== Starting MCP Server ===")
    print("  CLI:    scitex-dataset mcp start")
    print("  Python: fastmcp run scitex_dataset._mcp.server:mcp")
    print("  Tools:  scitex-dataset mcp list-tools")


if __name__ == "__main__":
    main()

# EOF
