# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Install package in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy greeummcp
```

### Running the Server
```bash
# Start MCP server (default: stdio transport, ./data directory)
greeummcp

# Start with custom data directory
greeummcp /path/to/data

# Start with HTTP transport
greeummcp --transport http --port 8000

# Legacy commands (still supported)
greeummcp run
greeum_mcp
```

### CLI Commands
```bash
# Show version
greeummcp version

# List available tools
greeummcp list-tools
```

## Architecture

GreeumMCP implements the Model Context Protocol (MCP) to provide memory capabilities to LLMs. The system bridges the Greeum Memory Engine (blockchain-based long-term memory and TTL-based short-term memory) with MCP-compatible clients.

### Core Components

1. **server.py**: Main MCP server that registers tools, resources, and prompts
2. **adapters/greeum_adapter.py**: Lazy-loads Greeum components (BlockManager, STMManager, etc.) and provides unified interface
3. **tools/memory_tools.py**: Implements memory operations (add, query, retrieve, update, delete)
4. **tools/utility_tools.py**: Provides utilities like prompt generation and blockchain verification

### Key Design Patterns

- **Lazy Initialization**: Greeum components are initialized only when first accessed
- **Singleton Adapter**: Single instance manages all Greeum component interactions
- **MCP Protocol**: All operations exposed through standard MCP tools/resources

### Memory System

- **Long-term Memory**: Stored in blockchain, permanent unless explicitly deleted
- **Short-term Memory (STM)**: TTL-based, automatically expires
- **Search**: Supports both semantic similarity and time-based queries
- **Enrichment**: Automatic keyword/tag extraction and importance scoring

## Testing

Tests are located in `tests/` directory. Run with `pytest`. The CI pipeline tests on Python 3.10 and 3.11.

## Entry Points

- **Console Scripts**: `greeummcp` (Typer CLI) and `greeum_mcp` (legacy)
- **Python API**: `from greeummcp import run_server`
- **Docker**: Dockerfile provided, defaults to HTTP transport on port 8000