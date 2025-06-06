#!/bin/bash
# Uninstall script for Unifi MCP Server

echo "Uninstalling Unifi MCP Server..."

# Check if Claude Desktop is configured with this server
if command -v python3 &> /dev/null; then
    echo "Checking Claude Desktop configuration..."
    if [ -f configure_claude.py ]; then
        # Add --remove option to configure_claude.py
        if ! grep -q "def remove_from_config" configure_claude.py; then
            echo "Adding remove option to configure_claude.py..."
            cat >> configure_claude.py << 'EOF'

def remove_from_config(config_path):
    """Remove the Unifi MCP server from Claude Desktop config"""
    if not config_path:
        print("Could not find Claude Desktop config file.")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Could not read Claude Desktop config file.")
        return False
    
    # Remove the unifi server config if it exists
    if 'mcpServers' in config and 'unifi' in config['mcpServers']:
        del config['mcpServers']['unifi']
        print("Removed Unifi MCP server from Claude Desktop config.")
        
        # Write the updated config
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing config file: {e}")
            return False
    else:
        print("Unifi MCP server not found in Claude Desktop config.")
        return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        config_path = find_claude_config()
        if remove_from_config(config_path):
            print("Successfully removed from Claude Desktop config.")
            print("Please restart Claude Desktop to apply the changes.")
        else:
            print("Failed to remove from Claude Desktop config.")
            sys.exit(1)
        sys.exit(0)
EOF
        fi
        
        python3 configure_claude.py --remove
    fi
fi

# Stop and remove Docker containers if they exist
if command -v docker-compose &> /dev/null && [ -f docker-compose.yml ]; then
    echo "Stopping and removing Docker containers..."
    docker-compose down
fi

# Ask for confirmation before removing files
echo ""
echo "This will remove all files in the current directory."
echo "Are you sure you want to continue? (y/n)"
read -r confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    # Remove virtual environment
    if [ -d .venv ]; then
        echo "Removing virtual environment..."
        rm -rf .venv
    fi
    
    # Remove all files except this script
    echo "Removing all files..."
    find . -type f -not -name "uninstall.sh" -delete
    find . -type d -not -name "." -not -name ".." -exec rm -rf {} +
    
    echo "Uninstall complete!"
    echo "You can now delete this directory and the uninstall script."
else
    echo "Uninstall cancelled."
fi