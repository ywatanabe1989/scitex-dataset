#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-01-29 22:45:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-dataset/src/scitex_dataset/_cli/__init__.py

"""Command-line interface for scitex-dataset."""

import json
from pathlib import Path

import click

from .. import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _print_command_help(cmd, prefix: str, parent_ctx) -> None:
    """Recursively print help for a command and its subcommands."""
    click.echo(f"\n{'=' * 50}")
    click.echo(f"{prefix}")
    click.echo("=" * 50)
    sub_ctx = click.Context(cmd, info_name=prefix.split()[-1], parent=parent_ctx)
    click.echo(cmd.get_help(sub_ctx))

    if isinstance(cmd, click.Group):
        for sub_name, sub_cmd in sorted(cmd.commands.items()):
            _print_command_help(sub_cmd, f"{prefix} {sub_name}", sub_ctx)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--version", "-V", is_flag=True, help="Show version and exit.")
@click.option("--help-recursive", is_flag=True, help="Show help for all commands.")
@click.pass_context
def main(ctx: click.Context, version: bool, help_recursive: bool) -> None:
    """scitex-dataset - Unified interface for scientific dataset discovery.

    Fetch and search datasets from neuroscience repositories:
    OpenNeuro, DANDI, PhysioNet, and more.
    """
    if version:
        click.echo(f"scitex-dataset {__version__}")
        ctx.exit(0)

    if help_recursive:
        click.echo(f"scitex-dataset {__version__}")
        click.echo(main.get_help(ctx))
        for name, cmd in sorted(main.commands.items()):
            _print_command_help(cmd, f"scitex-dataset {name}", ctx)
        ctx.exit(0)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# OpenNeuro command
@main.command()
@click.option("-n", "--max-datasets", default=0, help="Max datasets (0=all).")
@click.option("-b", "--batch-size", default=100, help="Datasets per request.")
@click.option("-o", "--output", type=click.Path(), help="Output JSON file.")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
def openneuro(max_datasets: int, batch_size: int, output: str, verbose: bool) -> None:
    """Fetch datasets from OpenNeuro (BIDS neuroimaging)."""
    from ..neuroscience.openneuro import fetch_all_datasets, format_dataset

    if verbose:
        click.echo("Fetching datasets from OpenNeuro...")

    datasets = fetch_all_datasets(
        batch_size=batch_size,
        max_datasets=max_datasets if max_datasets > 0 else None,
    )

    if not datasets:
        click.echo("No datasets fetched", err=True)
        raise SystemExit(1)

    formatted = [format_dataset(ds) for ds in datasets]

    if output:
        Path(output).write_text(json.dumps(formatted, indent=2))
        click.echo(f"Saved {len(formatted)} datasets to {output}")
    else:
        if verbose:
            for ds in formatted[:10]:
                click.echo(f"  {ds['id']}: {ds['name']} ({ds['n_subjects']} subjects)")
        click.echo(f"Fetched {len(formatted)} datasets")


# DANDI command
@main.command()
@click.option("-n", "--max-datasets", default=0, help="Max datasets (0=all).")
@click.option("-o", "--output", type=click.Path(), help="Output JSON file.")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
def dandi(max_datasets: int, output: str, verbose: bool) -> None:
    """Fetch datasets from DANDI Archive (NWB neurophysiology)."""
    from ..neuroscience.dandi import fetch_all_datasets, format_dataset

    if verbose:
        click.echo("Fetching dandisets from DANDI Archive...")

    datasets = fetch_all_datasets(
        max_datasets=max_datasets if max_datasets > 0 else None,
    )

    if not datasets:
        click.echo("No datasets fetched", err=True)
        raise SystemExit(1)

    formatted = [format_dataset(ds) for ds in datasets]

    if output:
        Path(output).write_text(json.dumps(formatted, indent=2))
        click.echo(f"Saved {len(formatted)} dandisets to {output}")
    else:
        if verbose:
            for ds in formatted[:10]:
                click.echo(f"  {ds['id']}: {ds['name']}")
        click.echo(f"Fetched {len(formatted)} dandisets")


# PhysioNet command
@main.command()
@click.option("-n", "--max-datasets", default=0, help="Max datasets (0=all).")
@click.option("-o", "--output", type=click.Path(), help="Output JSON file.")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
def physionet(max_datasets: int, output: str, verbose: bool) -> None:
    """Fetch datasets from PhysioNet (EEG/ECG/physiology)."""
    from ..neuroscience.physionet import fetch_all_datasets, format_dataset

    if verbose:
        click.echo("Fetching databases from PhysioNet...")

    datasets = fetch_all_datasets(
        max_datasets=max_datasets if max_datasets > 0 else None,
    )

    if not datasets:
        click.echo("No datasets fetched", err=True)
        raise SystemExit(1)

    formatted = [format_dataset(ds) for ds in datasets]

    if output:
        Path(output).write_text(json.dumps(formatted, indent=2))
        click.echo(f"Saved {len(formatted)} databases to {output}")
    else:
        if verbose:
            for ds in formatted[:10]:
                click.echo(f"  {ds['id']}: {ds['name']}")
        click.echo(f"Fetched {len(formatted)} databases")


# Database commands
@main.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--help-recursive", is_flag=True, help="Show help for all commands.")
@click.pass_context
def db(ctx: click.Context, help_recursive: bool):
    """Local database commands for fast searching."""
    if help_recursive:
        click.echo(db.get_help(ctx))
        for name, cmd in sorted(db.commands.items()):
            _print_command_help(cmd, f"scitex-dataset db {name}", ctx)
        ctx.exit(0)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@db.command("build")
@click.option(
    "-s",
    "--sources",
    multiple=True,
    type=click.Choice(["openneuro", "dandi", "physionet"]),
    help="Sources to index (default: all).",
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
def db_build(sources: tuple, verbose: bool) -> None:
    """Build/rebuild the local dataset database."""
    from .. import database

    source_list = list(sources) if sources else None

    if verbose:
        click.echo(f"Building database at {database.get_db_path()}")
        click.echo(f"Sources: {source_list or 'all'}")

    counts = database.build(sources=source_list)

    click.echo("Database built:")
    for src, count in counts.items():
        click.echo(f"  {src}: {count} datasets")
    click.echo(f"Total: {sum(counts.values())} datasets")


@db.command("search")
@click.argument("query", required=False)
@click.option("-s", "--source", type=click.Choice(["openneuro", "dandi", "physionet"]))
@click.option("-m", "--modality", help="Filter by modality (mri, eeg, etc.).")
@click.option("--min-subjects", type=int, help="Minimum subjects.")
@click.option("--max-subjects", type=int, help="Maximum subjects.")
@click.option("--min-downloads", type=int, help="Minimum downloads.")
@click.option("-n", "--limit", default=20, help="Max results (default: 20).")
@click.option("--order-by", default="downloads", help="Order by field.")
@click.option("-o", "--output", type=click.Path(), help="Output JSON file.")
def db_search(
    query: str,
    source: str,
    modality: str,
    min_subjects: int,
    max_subjects: int,
    min_downloads: int,
    limit: int,
    order_by: str,
    output: str,
) -> None:
    """Search the local database."""
    from .. import database

    results = database.search(
        query=query,
        source=source,
        modality=modality,
        min_subjects=min_subjects,
        max_subjects=max_subjects,
        min_downloads=min_downloads,
        limit=limit,
        order_by=order_by,
    )

    if not results:
        click.echo("No datasets found.")
        return

    if output:
        Path(output).write_text(json.dumps(results, indent=2))
        click.echo(f"Saved {len(results)} results to {output}")
    else:
        for ds in results:
            n_sub = ds.get("n_subjects", 0)
            downloads = ds.get("downloads", 0)
            click.echo(f"  {ds['id']}: {ds.get('name', 'N/A')[:50]}")
            click.echo(f"    subjects={n_sub}, downloads={downloads}")
        click.echo(f"\nFound {len(results)} datasets")


@db.command("stats")
def db_stats() -> None:
    """Show database statistics."""
    from .. import database

    stats = database.get_stats()

    if not stats.get("exists"):
        click.echo(stats.get("message", "Database not found."))
        click.echo("Run: scitex-dataset db build")
        return

    click.echo(f"Database: {stats['path']}")
    click.echo(f"Size: {stats['size_mb']} MB")
    click.echo(f"Total datasets: {stats['total_datasets']}")
    click.echo(f"Last build: {stats.get('last_build', 'N/A')}")
    click.echo("\nBy source:")
    for src, count in stats.get("by_source", {}).items():
        click.echo(f"  {src}: {count}")


@db.command("clear")
@click.confirmation_option(prompt="Delete the local database?")
def db_clear() -> None:
    """Delete the local database."""
    from .. import database

    if database.clear():
        click.echo("Database deleted.")
    else:
        click.echo("Database not found.")


# MCP commands
@main.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--help-recursive", is_flag=True, help="Show help for all commands.")
@click.pass_context
def mcp(ctx: click.Context, help_recursive: bool):
    """MCP (Model Context Protocol) server commands."""
    if help_recursive:
        click.echo(mcp.get_help(ctx))
        for name, cmd in sorted(mcp.commands.items()):
            _print_command_help(cmd, f"scitex-dataset mcp {name}", ctx)
        ctx.exit(0)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@mcp.command("start")
def mcp_start() -> None:
    """Start the scitex-dataset MCP server."""
    try:
        from .._mcp.server import mcp as mcp_server
    except ImportError as e:
        raise click.ClickException(
            f"fastmcp not installed. Install: pip install scitex-dataset[mcp]\n{e}"
        ) from e

    click.echo("Starting scitex-dataset MCP server...")
    mcp_server.run()


def _format_signature(tool) -> str:
    """Format tool as Python-like function signature."""
    params = []
    if hasattr(tool, "parameters") and tool.parameters:
        schema = tool.parameters
        props = schema.get("properties", {})
        required = schema.get("required", [])
        for name, info in props.items():
            ptype = info.get("type", "any")
            default = info.get("default")
            if name in required:
                params.append(f"{name}: {ptype}")
            elif default is not None:
                params.append(f"{name}: {ptype} = {default!r}")
            else:
                params.append(f"{name}: {ptype} = None")
    return f"{tool.name}({', '.join(params)})"


def _estimate_tokens(text: str) -> int:
    """Estimate token count (rough: ~4 chars per token)."""
    return len(text) // 4 if text else 0


def _get_mcp_summary(mcp_server) -> dict:
    """Get MCP server summary statistics."""
    tools = list(mcp_server._tool_manager._tools.values())

    # Calculate total context size
    instructions = getattr(mcp_server, "instructions", "") or ""
    total_desc = sum(len(t.description or "") for t in tools)
    total_params = sum(
        len(json.dumps(t.parameters))
        if hasattr(t, "parameters") and t.parameters
        else 0
        for t in tools
    )

    return {
        "name": getattr(mcp_server, "name", "unknown"),
        "tool_count": len(tools),
        "instructions_chars": len(instructions),
        "instructions_tokens": _estimate_tokens(instructions),
        "descriptions_chars": total_desc,
        "descriptions_tokens": _estimate_tokens("x" * total_desc),
        "schemas_chars": total_params,
        "schemas_tokens": _estimate_tokens("x" * total_params),
        "total_context_tokens": (
            _estimate_tokens(instructions)
            + _estimate_tokens("x" * total_desc)
            + _estimate_tokens("x" * total_params)
        ),
    }


@mcp.command("list-tools")
@click.option("-v", "--verbose", count=True, help="Verbosity: -v, -vv, -vvv.")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON.")
@click.option("--summary", "show_summary", is_flag=True, help="Show context summary.")
def mcp_list_tools(verbose: int, as_json: bool, show_summary: bool) -> None:
    """List available MCP tools.

    Verbosity: (none) names, -v signatures, -vv +description, -vvv full.
    """
    try:
        from .._mcp.server import mcp as mcp_server
    except ImportError as e:
        raise click.ClickException(
            f"fastmcp not installed. Install: pip install scitex-dataset[mcp]\n{e}"
        ) from e

    tools = list(mcp_server._tool_manager._tools.values())
    summary = _get_mcp_summary(mcp_server)

    if as_json:
        tool_data = []
        for tool in tools:
            schema = tool.parameters if hasattr(tool, "parameters") else {}
            tool_data.append(
                {
                    "name": tool.name,
                    "signature": _format_signature(tool),
                    "description": tool.description,
                    "parameters": schema,
                }
            )
        output = {"summary": summary, "tools": tool_data}
        click.echo(json.dumps(output, indent=2))
        return

    # Header with summary
    click.echo(f"MCP Server: {summary['name']}")
    click.echo(f"Tools: {summary['tool_count']}")
    if show_summary:
        click.echo(f"Context: ~{summary['total_context_tokens']:,} tokens")
        click.echo(f"  Instructions: ~{summary['instructions_tokens']:,} tokens")
        click.echo(f"  Descriptions: ~{summary['descriptions_tokens']:,} tokens")
        click.echo(f"  Schemas: ~{summary['schemas_tokens']:,} tokens")
    click.echo()

    for tool in tools:
        if verbose == 0:
            # Names only
            click.echo(f"  {tool.name}")
        elif verbose == 1:
            # Full signature
            click.echo(f"  {_format_signature(tool)}")
        elif verbose == 2:
            # Signature + one-line description
            click.echo(f"  {_format_signature(tool)}")
            if tool.description:
                desc = tool.description.split("\n")[0].strip()
                click.echo(f"    {desc}")
            click.echo()
        else:
            # Signature + full description
            click.echo(f"  {_format_signature(tool)}")
            if tool.description:
                for line in tool.description.strip().split("\n"):
                    click.echo(f"    {line}")
            click.echo()


@mcp.command("doctor")
def mcp_doctor() -> None:
    """Check MCP server dependencies."""
    click.echo("Checking MCP dependencies...")

    try:
        import fastmcp

        click.echo(f"  OK fastmcp {fastmcp.__version__}")
    except ImportError:
        click.echo("  NG fastmcp not installed")
        click.echo("     Install: pip install scitex-dataset[mcp]")
        return

    try:
        from .._mcp.server import mcp as mcp_server

        click.echo(f"  OK MCP server ({len(mcp_server._tool_manager._tools)} tools)")
    except Exception as exc:
        click.echo(f"  NG MCP server error: {exc}")
        return

    click.echo("\nMCP server ready. Run: scitex-dataset mcp run")


@mcp.command("install")
@click.option("--claude-code", is_flag=True, help="Show Claude Code config.")
def mcp_install(claude_code: bool) -> None:
    """Show MCP installation instructions."""
    if claude_code:
        click.echo("Add to Claude Code MCP config:")
        click.echo()
        click.echo('  "scitex-dataset": {')
        click.echo('    "command": "scitex-dataset",')
        click.echo('    "args": ["mcp", "run"]')
        click.echo("  }")
    else:
        click.echo("scitex-dataset MCP Server Installation")
        click.echo("=" * 40)
        click.echo()
        click.echo("1. Install: pip install scitex-dataset[mcp]")
        click.echo("2. Config:  scitex-dataset mcp install --claude-code")
        click.echo("3. Test:    scitex-dataset mcp doctor")


if __name__ == "__main__":
    main()

# EOF
