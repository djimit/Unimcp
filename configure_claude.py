#!/usr/bin/env python3
"""
Helper script to configure Claude Desktop for Unifi MCP Server
"""
import json
import sys
import subprocess
from pathlib import Path


def find_uv_path():
    """Find the path to the uv executable"""
    try:
        result = subprocess.run(
            ["which", "uv"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def find_claude_config():
    """Find the Claude Desktop config file"""
    home = Path.home()
    
    # Common locations for Claude Desktop config
    possible_paths = [
        home / "Library" / "Application Support" / "Claude" /
        "claude_desktop_config.json",
        home / ".config" / "Claude" / "claude_desktop_config.json",
        home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


def update_claude_config(config_path, uv_path, server_dir):
    """Update the Claude Desktop config file"""
    if not config_path:
        print("Could not find Claude Desktop config file.")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {}
    
    # Ensure mcpServers exists
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    
    # Add or update the unifi server config
    config['mcpServers']['unifi'] = {
        "command": uv_path,
        "args": [
            "--directory",
            str(server_dir),
            "run",
            "main.py"
        ]
    }
    
    # Write the updated config
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error writing config file: {e}")
        return False


def main():
    """Main function"""
    print("Configuring Claude Desktop for Unifi MCP Server...")
    
    # Find the uv executable
    uv_path = find_uv_path()
    if not uv_path:
        print("Could not find 'uv' executable. Please install it or add it to "
              "your PATH.")
        sys.exit(1)
    
    print(f"Found uv at: {uv_path}")
    
    # Get the current directory (where the MCP server is installed)
    server_dir = Path.cwd().absolute()
    print(f"Using server directory: {server_dir}")
    
    # Find the Claude Desktop config file
    config_path = find_claude_config()
    if not config_path:
        print("Could not find Claude Desktop config file.")
        print("Please manually add the MCP server to your Claude Desktop "
              "config.")
        print(f"""
Add the following to your Claude Desktop config:
{{
  "mcpServers": {{
    "unifi": {{
      "command": "{uv_path}",
      "args": [
        "--directory",
        "{server_dir}",
        "run",
        "main.py"
      ]
    }}
  }}
}}
""")
        sys.exit(1)
    
    print(f"Found Claude Desktop config at: {config_path}")
    
    # Update the config
    if update_claude_config(config_path, uv_path, server_dir):
        print("Successfully updated Claude Desktop config!")
        print("Please restart Claude Desktop to apply the changes.")
    else:
        print("Failed to update Claude Desktop config.")
        sys.exit(1)


if __name__ == "__main__":
    main()