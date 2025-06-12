#!/usr/bin/env python
"""
GreeumMCP Claude Desktop Integration Example

This example shows how to setup GreeumMCP for use with Claude Desktop.
It outputs instructions for configuring Claude Desktop to use GreeumMCP.
"""
import os
import sys
import json
import argparse
import platform

# Add parent directory to path to import greeummcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def get_config_path():
    """Get the Claude Desktop config file path for the current platform."""
    if platform.system() == "Windows":
        return os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json")
    elif platform.system() == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:  # Linux
        return os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

def get_absolute_package_path():
    """Get absolute path to the GreeumMCP package."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def create_config_file(data_dir, use_simple_command=True):
    """Create Claude Desktop config file."""
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Try to detect if greeummcp is installed
    try:
        import subprocess
        result = subprocess.run(['greeummcp', 'version'], capture_output=True, text=True)
        greeummcp_installed = result.returncode == 0
    except:
        greeummcp_installed = False
    
    # Create config with appropriate command
    if greeummcp_installed and use_simple_command:
        # Use simplified command when greeummcp is installed
        if data_dir == "./data":
            # Use default data directory
            config = {
                "mcpServers": {
                    "greeum_mcp": {
                        "command": "greeummcp.exe" if platform.system() == "Windows" else "greeummcp"
                    }
                }
            }
        else:
            # Use custom data directory
            config = {
                "mcpServers": {
                    "greeum_mcp": {
                        "command": "greeummcp.exe" if platform.system() == "Windows" else "greeummcp",
                        "args": [data_dir]
                    }
                }
            }
    else:
        # Fallback to Python script execution
        entry_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'greeummcp', 'server.py'))
        config = {
            "mcpServers": {
                "greeum_mcp": {
                    "command": "python" if platform.system() == "Windows" else "python3",
                    "args": [
                        entry_script,
                        "--data-dir", data_dir,
                        "--transport", "stdio"
                    ]
                }
            }
        }
    
    # Write config to file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    return config_path

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="GreeumMCP Claude Desktop Integration")
    parser.add_argument("--data-dir", default="./data", help="Data directory")
    parser.add_argument("--entry-script", help="Custom entry script")
    parser.add_argument("--check", action="store_true", help="Check if Claude Desktop config file exists")
    parser.add_argument("--create", action="store_true", help="Create Claude Desktop config file")
    parser.add_argument("--print", action="store_true", help="Print configuration without creating file")
    
    args = parser.parse_args()
    
    # Make data directory absolute
    data_dir = os.path.abspath(args.data_dir)
    os.makedirs(data_dir, exist_ok=True)
    
    # Get Claude Desktop config path
    config_path = get_config_path()
    
    # Check if config file exists
    if args.check:
        if os.path.exists(config_path):
            print_colored(f"Claude Desktop config file exists at: {config_path}", "green")
            
            # Check if it contains GreeumMCP configuration
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                if "mcpServers" in config and "greeum_mcp" in config["mcpServers"]:
                    print_colored("GreeumMCP is configured in Claude Desktop!", "green")
                else:
                    print_colored("Claude Desktop config file does not contain GreeumMCP configuration.", "yellow")
            except Exception as e:
                print_colored(f"Error reading config file: {e}", "red")
        else:
            print_colored(f"Claude Desktop config file not found at: {config_path}", "yellow")
        return
    
    # Create config file
    if args.create:
        try:
            created_path = create_config_file(data_dir)
            print_colored(f"Claude Desktop config file created at: {created_path}", "green")
            print_colored("Please restart Claude Desktop to apply the changes.", "cyan")
        except Exception as e:
            print_colored(f"Error creating config file: {e}", "red")
        return
    
    # Just print the configuration
    if args.print:
        # Try to detect if greeummcp is installed
        try:
            import subprocess
            result = subprocess.run(['greeummcp', 'version'], capture_output=True, text=True)
            greeummcp_installed = result.returncode == 0
        except:
            greeummcp_installed = False
        
        print_colored("Configuration for Claude Desktop:", "cyan")
        
        if greeummcp_installed:
            # Show simplified config
            if data_dir == "./data":
                config = {
                    "mcpServers": {
                        "greeum_mcp": {
                            "command": "greeummcp.exe" if platform.system() == "Windows" else "greeummcp"
                        }
                    }
                }
            else:
                config = {
                    "mcpServers": {
                        "greeum_mcp": {
                            "command": "greeummcp.exe" if platform.system() == "Windows" else "greeummcp",
                            "args": [data_dir]
                        }
                    }
                }
        else:
            # Show fallback config
            entry_script = args.entry_script
            if entry_script is None:
                entry_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'greeummcp', 'server.py'))
            
            config = {
                "mcpServers": {
                    "greeum_mcp": {
                        "command": "python" if platform.system() == "Windows" else "python3",
                        "args": [
                            entry_script,
                            "--data-dir", data_dir,
                            "--transport", "stdio"
                        ]
                    }
                }
            }
        
        print(json.dumps(config, indent=4))
        print_colored(f"\nConfig file path: {config_path}", "cyan")
        return
    
    # Print instructions
    print_colored("=== GreeumMCP Claude Desktop Integration ===", "cyan")
    print_colored("\nFollow these steps to integrate GreeumMCP with Claude Desktop:", "white")
    print()
    print_colored("1. Make sure Claude Desktop is installed", "yellow")
    print("   Download from: https://claude.ai/desktop")
    print()
    print_colored("2. Create Claude Desktop config file:", "yellow")
    print(f"   python {os.path.basename(__file__)} --create --data-dir=<your-data-dir>")
    print()
    print_colored("3. Restart Claude Desktop", "yellow")
    print()
    print_colored("4. Test the integration with Claude Desktop", "yellow")
    print("   - Open Claude Desktop")
    print("   - Look for the tools icon (hammer) in the interface")
    print("   - Try using the memory tools with prompts like:")
    print("     * 'Save this information: Python was created by Guido van Rossum'")
    print("     * 'What information do you have about Python?'")
    print()
    print_colored("For more details, run:", "magenta")
    print(f"  python {os.path.basename(__file__)} --help")

if __name__ == "__main__":
    main() 