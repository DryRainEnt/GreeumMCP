"""
Greeum MCP Server Implementation
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

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
        
        # Register MCP tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools."""
        @self.mcp.tool()
        async def server_status() -> Dict[str, Any]:
            """Get the server status.
            
            Returns:
                Server status information
            """
            import time
            import os
            
            return {
                "server_name": self.server_name,
                "data_directory": self.data_dir,
                "transport": self.transport,
                "status": "running"
            }
            
        @self.mcp.tool()
        async def add_memory(content: str, importance: float = 0.5) -> str:
            """Add a new memory to the long-term storage.
            
            Args:
                content: The content of the memory to store
                importance: The importance of the memory (0.0-1.0)
            
            Returns:
                Memory ID of the created memory
            """
            import os
            import time
            import json
            import uuid
            
            memory_id = str(uuid.uuid4())
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            memory = {
                "id": memory_id,
                "content": content,
                "timestamp": timestamp,
                "importance": importance
            }
            
            # 간단한 파일 기반 저장
            os.makedirs(self.data_dir, exist_ok=True)
            with open(os.path.join(self.data_dir, f"{memory_id}.json"), "w") as f:
                json.dump(memory, f)
            
            return memory_id
            
        @self.mcp.tool()
        async def query_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
            """Search memories by query text.
            
            Args:
                query: The search query
                limit: Maximum number of results to return
            
            Returns:
                List of matching memory blocks
            """
            import os
            import json
            import glob
            
            memories = []
            
            # 간단한 파일 기반 검색
            memory_files = glob.glob(os.path.join(self.data_dir, "*.json"))
            for memory_file in memory_files[:limit]:
                try:
                    with open(memory_file, "r") as f:
                        memory = json.load(f)
                        if query.lower() in memory.get("content", "").lower():
                            memories.append(memory)
                except Exception:
                    continue
            
            return memories
    
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