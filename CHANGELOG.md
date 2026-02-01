# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-29

### Added
- Initial release
- OpenNeuro dataset fetching and search
- DANDI Archive integration
- PhysioNet database support
- Unified search across repositories
- CLI with `openneuro`, `dandi`, `physionet`, `search` commands
- MCP server with 8 tools for AI agent integration
- Database module for local caching
- SciTeX session integration support

### MCP Tools
- `dataset_openneuro_fetch` - Fetch OpenNeuro datasets
- `dataset_openneuro_search` - Search OpenNeuro
- `dataset_dandi_fetch` - Fetch DANDI datasets
- `dataset_dandi_search` - Search DANDI
- `dataset_physionet_fetch` - Fetch PhysioNet datasets
- `dataset_physionet_search` - Search PhysioNet
- `dataset_search` - Unified cross-repository search
- `dataset_stats` - Repository statistics
