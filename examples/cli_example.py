#!/usr/bin/env python
"""
GreeumMCP CLI Example

This example demonstrates how to use GreeumMCP from the command line.
"""
import os
import sys
import argparse
import time
import json
from typing import Dict, Any, List

# Add parent directory to path to import greeummcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from greeummcp import GreeumMCPServer

def print_colored(text: str, color: str = "white"):
    """Print colored text."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def format_memory(memory: Dict[str, Any]) -> str:
    """Format a memory for display."""
    result = []
    result.append(f"ID: {memory.get('id', '')}")
    result.append(f"Content: {memory.get('content', '')}")
    result.append(f"Timestamp: {memory.get('timestamp', '')}")
    
    if "keywords" in memory and memory["keywords"]:
        result.append(f"Keywords: {', '.join(memory.get('keywords', []))}")
    
    if "importance" in memory:
        result.append(f"Importance: {memory.get('importance', 0.0)}")
    
    return "\n".join(result)

def interactive_mode(server: GreeumMCPServer):
    """Run interactive mode."""
    print_colored("=== GreeumMCP Interactive Mode ===", "cyan")
    print_colored("Type 'help' to see available commands, 'exit' to quit", "yellow")
    
    while True:
        try:
            command = input("\ngreeum> ").strip()
            
            if command.lower() == "exit":
                break
            
            if command.lower() == "help":
                print_help()
                continue
            
            if command.lower() == "status":
                status = server.mcp._tools["server_status"].func()
                print_colored("Server Status:", "cyan")
                for key, value in status.items():
                    print(f"  {key}: {value}")
                continue
            
            if command.lower().startswith("add "):
                content = command[4:].strip()
                if not content:
                    print_colored("Error: Memory content required", "red")
                    continue
                
                memory_id = server.mcp._tools["add_memory"].func(content)
                print_colored(f"Memory added with ID: {memory_id}", "green")
                continue
            
            if command.lower().startswith("get "):
                memory_id = command[4:].strip()
                if not memory_id:
                    print_colored("Error: Memory ID required", "red")
                    continue
                
                memory = server.mcp._tools["retrieve_memory"].func(memory_id)
                if "error" in memory:
                    print_colored(f"Error: {memory['error']}", "red")
                else:
                    print_colored("Memory:", "cyan")
                    print(format_memory(memory))
                continue
            
            if command.lower().startswith("search "):
                query = command[7:].strip()
                if not query:
                    print_colored("Error: Search query required", "red")
                    continue
                
                results = server.mcp._tools["query_memory"].func(query)
                if not results:
                    print_colored("No results found", "yellow")
                else:
                    print_colored(f"Found {len(results)} results:", "cyan")
                    for i, memory in enumerate(results):
                        print(f"\n--- Result {i+1} ---")
                        print(format_memory(memory))
                continue
            
            if command.lower().startswith("time "):
                query = command[5:].strip()
                if not query:
                    print_colored("Error: Time query required", "red")
                    continue
                
                results = server.mcp._tools["search_time"].func(query)
                if not results:
                    print_colored("No results found", "yellow")
                else:
                    print_colored(f"Found {len(results)} results:", "cyan")
                    for i, memory in enumerate(results):
                        print(f"\n--- Result {i+1} ---")
                        print(format_memory(memory))
                continue
            
            print_colored(f"Unknown command: {command}", "red")
            print_colored("Type 'help' to see available commands", "yellow")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print_colored(f"Error: {str(e)}", "red")

def print_help():
    """Print help information."""
    print_colored("\nAvailable Commands:", "cyan")
    print("  help               - Show this help message")
    print("  exit               - Exit the program")
    print("  status             - Show server status")
    print("  add <content>      - Add a new memory")
    print("  get <id>           - Get a memory by ID")
    print("  search <query>     - Search memories by query")
    print("  time <query>       - Search memories by time reference")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="GreeumMCP CLI Example")
    parser.add_argument("--data-dir", default="./data", help="Data directory")
    parser.add_argument("--add", help="Add a memory and exit")
    parser.add_argument("--search", help="Search memories and exit")
    parser.add_argument("--time", help="Search memories by time reference and exit")
    parser.add_argument("--get", help="Get memory by ID and exit")
    parser.add_argument("--status", action="store_true", help="Show server status and exit")
    
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    os.makedirs(args.data_dir, exist_ok=True)
    
    # Initialize server
    server = GreeumMCPServer(
        data_dir=args.data_dir,
        server_name="greeum",
        port=8000,
        transport="stdio"
    )
    
    # Initialize Greeum components
    server._init_greeum_components()
    
    # Register tools
    server._register_tools()
    
    # Handle command-line actions
    if args.add:
        memory_id = server.mcp._tools["add_memory"].func(args.add)
        print_colored(f"Memory added with ID: {memory_id}", "green")
        return
    
    if args.search:
        results = server.mcp._tools["query_memory"].func(args.search)
        if not results:
            print_colored("No results found", "yellow")
        else:
            print_colored(f"Found {len(results)} results:", "cyan")
            for i, memory in enumerate(results):
                print(f"\n--- Result {i+1} ---")
                print(format_memory(memory))
        return
    
    if args.time:
        results = server.mcp._tools["search_time"].func(args.time)
        if not results:
            print_colored("No results found", "yellow")
        else:
            print_colored(f"Found {len(results)} results:", "cyan")
            for i, memory in enumerate(results):
                print(f"\n--- Result {i+1} ---")
                print(format_memory(memory))
        return
    
    if args.get:
        memory = server.mcp._tools["retrieve_memory"].func(args.get)
        if "error" in memory:
            print_colored(f"Error: {memory['error']}", "red")
        else:
            print_colored("Memory:", "cyan")
            print(format_memory(memory))
        return
    
    if args.status:
        status = server.mcp._tools["server_status"].func()
        print_colored("Server Status:", "cyan")
        for key, value in status.items():
            print(f"  {key}: {value}")
        return
    
    # If no command-line actions, run interactive mode
    interactive_mode(server)

if __name__ == "__main__":
    main() 