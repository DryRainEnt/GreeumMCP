import typer
from typing import Optional
from .server import GreeumMCPServer
from . import __version__

app = typer.Typer(add_completion=False, help="GreeumMCP command-line interface")

@app.command()
def version():
    """Print GreeumMCP version."""
    typer.echo(__version__)

@app.command()
def list_tools(data_dir: str = typer.Option("./data"), transport: str = typer.Option("stdio")):
    """Show available MCP tool names (without starting the server)."""
    server = GreeumMCPServer(data_dir=data_dir, transport=transport)
    tool_names = list(server.mcp._tools.keys())  # FastMCP internal registry
    typer.echo("\n".join(tool_names))

@app.command()
def run(
    data_dir: str = typer.Option("./data", help="Memory data directory"),
    server_name: str = typer.Option("greeum_mcp", help="Server name"),
    port: int = typer.Option(8000, help="Port for http/websocket"),
    transport: str = typer.Option("stdio", help="Transport type: stdio|http|websocket"),
):
    """Run GreeumMCP server."""
    server = GreeumMCPServer(
        data_dir=data_dir,
        server_name=server_name,
        port=port,
        transport=transport,
    )
    server.run()

if __name__ == "__main__":
    app() 