# GreeumMCP

GreeumMCP is a Model Context Protocol (MCP) server implementation for the Greeum Memory Engine. It enables seamless integration of Greeum's powerful memory capabilities with Large Language Models (LLMs) that support the MCP standard, such as Claude.

## Features

- **Memory Management**: Store, retrieve, and search through long-term and short-term memories
- **Time-based Recall**: Search memories based on temporal references like "yesterday" or "two weeks ago"
- **Semantic Search**: Find memories based on semantic similarity
- **Memory Enrichment**: Automatically extract keywords, tags, and compute importance scores
- **Multiple Transport Options**: Supports stdio, HTTP, and WebSocket transports
- **Claude Desktop Integration**: Ready to use with Claude Desktop

## Installation

### Prerequisites

- Python 3.10 or higher
- Greeum 0.5.2 or higher
- MCP Python SDK 1.0.0 or higher

### Installation Methods

#### From PyPI (Recommended)

```bash
pip install greeummcp
```

#### From Source

```bash
git clone https://github.com/GreeumAI/GreeumMCP.git
cd GreeumMCP
pip install -e .
```

## Quick Start

### Running as a Command-Line Tool

GreeumMCP can be run directly from the command line:

```bash
# Using stdio transport (default)
greeum_mcp --data-dir ./data --transport stdio

# Using HTTP transport
greeum_mcp --data-dir ./data --transport http --port 8000
```

### Using as a Python Library

```python
from greeummcp import run_server

# Run with default settings
run_server()

# Run with custom settings
run_server(
    data_dir="./data",
    server_name="greeum_mcp",
    port=8000,
    transport="http",
    greeum_config={
        "ttl_short": 3600,  # 1 hour
        "ttl_medium": 86400,  # 1 day
        "ttl_long": 604800,  # 1 week
        "default_language": "auto"
    }
)
```

## Claude Desktop Integration

GreeumMCP can be used with Claude Desktop to provide memory capabilities to Claude. The package includes a helper script to set up the integration:

```bash
# Run the Claude Desktop integration helper
python examples/claude_desktop.py

# Create the Claude Desktop configuration file
python examples/claude_desktop.py --create --data-dir ./data
```

After setting up, restart Claude Desktop, and you should see the GreeumMCP tools available in the tools panel (hammer icon).

### Manual Configuration for Claude Desktop

You can also manually configure Claude Desktop to use GreeumMCP by creating a JSON configuration file:

1. Locate or create the Claude Desktop configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the GreeumMCP server configuration to this file:

#### Windows Example:
```json
{
    "mcpServers": {
        "greeum_mcp": {
            "command": "python",
            "args": [
                "-m", "greeummcp.server",
                "--data-dir", "C:\\Users\\USERNAME\\Documents\\greeum-data",
                "--transport", "stdio"
            ]
        }
    }
}
```

#### macOS/Linux Example:
```json
{
    "mcpServers": {
        "greeum_mcp": {
            "command": "python3",
            "args": [
                "-m", "greeummcp.server",
                "--data-dir", "/Users/USERNAME/Documents/greeum-data",
                "--transport", "stdio"
            ]
        }
    }
}
```

3. Make sure to replace `USERNAME` and adjust paths according to your system.
4. Restart Claude Desktop to apply the changes.
5. Verify that the tools are available by looking for the hammer icon in the Claude Desktop interface.

### Cursor Integration

To use GreeumMCP with Cursor, create a `.cursor/mcp.json` file in your project root:

```json
{
  "greeum_mcp": {
    "command": "python",
    "args": ["-m", "greeummcp.server", "--data-dir", "YOUR_DATA_DIR", "--transport", "stdio", "--server-name", "greeum_mcp"]
  }
}
```

#### Important Notes

- **Server naming**: Always use underscores (`_`) instead of hyphens (`-`) in server names to avoid MCP compatibility issues.
- **Data directory**: Use an absolute path for the data directory to ensure reliability.

### Verifying the Integration

To verify that GreeumMCP is working properly with Claude Desktop:

1. Click the hammer icon in Claude Desktop.
2. You should see GreeumMCP tools listed (like add_memory, query_memory, etc.).
3. Try adding a memory with a query like "Save this information: Claude was developed by Anthropic."
4. Then try retrieving it with "What information do you have about Claude?"

If you encounter issues:
- Check Claude Desktop logs in `~/Library/Logs/Claude/` (macOS) or `%APPDATA%\Claude\Logs` (Windows)
- Ensure the GreeumMCP server is properly installed and paths are correct
- Verify your configuration file has the correct syntax

## Memory Tools

GreeumMCP provides the following memory-related tools:

- **add_memory**: Add a new memory to long-term storage
- **query_memory**: Search memories by query text
- **retrieve_memory**: Retrieve a specific memory by ID
- **update_memory**: Update an existing memory
- **delete_memory**: Delete a memory by ID
- **search_time**: Search memories based on time references
- **generate_prompt**: Generate a prompt that includes relevant memories
- **extract_keywords**: Extract keywords from text
- **verify_chain**: Verify the integrity of the memory blockchain
- **server_status**: Get server status information

## Example Usage

### Interactive CLI

GreeumMCP includes an interactive CLI example for trying out the memory capabilities:

```bash
python examples/cli_example.py --data-dir ./data
```

This opens an interactive shell where you can:

```
greeum> add This is my first memory
Memory added with ID: 1

greeum> add This is my second memory about Python
Memory added with ID: 2

greeum> search Python
Found 1 results:

--- Result 1 ---
ID: 2
Content: This is my second memory about Python
Timestamp: 2023-07-01T12:34:56
Keywords: memory, Python, second
Importance: 0.65
```

## Development

### Project Structure

```
GreeumMCP/
├── greeummcp/                   # Main package
│   ├── __init__.py              # Package initialization
│   ├── server.py                # MCP server implementation
│   ├── tools/                   # MCP tools implementation
│   ├── resources/               # MCP resources implementation
│   ├── prompts/                 # MCP prompts implementation
│   └── adapters/                # Greeum integration adapters
├── examples/                    # Usage examples
├── tests/                       # Tests
├── README.md                    # Project documentation
├── setup.py                     # Package setup
└── requirements.txt             # Dependencies
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

GreeumMCP is licensed under the MIT License.

## Acknowledgments

- GreeumMCP is built on the [Model Context Protocol](https://modelcontextprotocol.io) standard
- GreeumMCP uses the [Greeum Memory Engine](https://github.com/GreeumAI/Greeum) as its core component
