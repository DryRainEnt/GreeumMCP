"""
Greeum MCP Server Implementation
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from .adapters.greeum_adapter import GreeumAdapter
from .tools.memory_tools import MemoryTools
from .tools.utility_tools import UtilityTools
import asyncio

class GreeumMCPServer:
    """
    GreeumMCP main server class that wraps Greeum memory engine with Model Context Protocol.
    
    This server provides tools to interact with Greeum's memory capabilities including:
    - Managing long-term memories (BlockManager)
    - Managing short-term memories (STMManager)
    - Cache management (CacheManager)
    - Temporal reasoning (TemporalReasoner)
    - Text processing utilities
    """
    
    def __init__(
        self,
        data_dir: str = "./data",
        server_name: str = "greeum_mcp",
        port: int = 8000,
        transport: str = "stdio",
        greeum_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize GreeumMCP server.
        
        Args:
            data_dir: Directory to store memory data
            server_name: Name of the MCP server
            port: Port for HTTP transport (if used)
            transport: Transport type ('stdio', 'http', 'websocket')
            greeum_config: Additional configuration for Greeum components
        """
        self.data_dir = data_dir
        self.server_name = server_name
        self.port = port
        self.transport = transport
        self.greeum_config = greeum_config or {}
        
        # Initialize MCP server with description
        from greeummcp import __version__
        self.mcp = FastMCP(
            self.server_name, 
            description="Greeum Memory Engine - Memory management for LLMs"
        )
        
        # Initialize Greeum adapter
        self.adapter = GreeumAdapter(
            data_dir=self.data_dir,
            greeum_config=self.greeum_config
        )

        # Lazily initialize Greeum core components (BlockManager 등)
        # Adapter 자체가 내부에서 initialize() 호출하도록 설계돼 있으므로 필요 시 자동 초기화됨.

        # Prepare tools instances
        self._memory_tools = MemoryTools(
            self.adapter.block_manager,
            self.adapter.stm_manager,
            self.adapter.cache_manager,
            self.adapter.temporal_reasoner
        )
        self._utility_tools = UtilityTools(
            self.adapter.block_manager,
            self.adapter.stm_manager,
            self.adapter.cache_manager,
            self.adapter.prompt_wrapper,
            self.data_dir
        )

        # Register MCP tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools from MemoryTools and UtilityTools dynamically."""

        def _register_from(obj):
            for attr_name in dir(obj):
                if attr_name.startswith("_"):
                    continue
                fn = getattr(obj, attr_name)
                if callable(fn) and asyncio.iscoroutinefunction(fn):
                    # Use existing docstring for tool description if present
                    self.mcp.tool(name=attr_name)(fn)

        # Register tools from both utility classes
        _register_from(self._memory_tools)
        _register_from(self._utility_tools)
    
    def run(self):
        """Run the MCP server with the configured transport."""
        if self.transport == "stdio":
            self.mcp.run(transport="stdio")
        elif self.transport == "http":
            self.mcp.run(transport="http", port=self.port)
        elif self.transport == "websocket":
            self.mcp.run(transport="websocket", port=self.port)
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")

# CLI entry point
def main():
    """CLI entry point for running the server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GreeumMCP Server")
    parser.add_argument("--data-dir", default="./data", help="Data directory")
    parser.add_argument("--server-name", default="greeum_mcp", help="Server name")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP/WS transport")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http", "websocket"], 
                        help="Transport type")
    
    args = parser.parse_args()
    
    server = GreeumMCPServer(
        data_dir=args.data_dir,
        server_name=args.server_name,
        port=args.port,
        transport=args.transport
    )
    
    server.run()

if __name__ == "__main__":
    main() 