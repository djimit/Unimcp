#!/bin/bash
# Status script for Unifi MCP Server

echo "Checking Unifi MCP Server status..."

# Check if the server is running locally
if pgrep -f "python main.py" > /dev/null; then
    echo "Server is running locally"
    
    # Get the process ID
    pid=$(pgrep -f "python main.py")
    echo "Process ID: $pid"
    
    # Get the port
    port=$(netstat -tlnp 2>/dev/null | grep "$pid" | awk '{print $4}' | cut -d: -f2)
    if [ -n "$port" ]; then
        echo "Listening on port: $port"
        echo "Server URL: http://localhost:$port"
        
        # Check if the API is responding
        if command -v curl &> /dev/null; then
            response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/docs)
            if [ "$response" == "200" ]; then
                echo "API is responding (HTTP 200 OK)"
            else
                echo "API is not responding properly (HTTP $response)"
            fi
        fi
    else
        echo "Could not determine port"
    fi
else
    echo "Server is not running locally"
fi

# Check if the server is running in Docker
if command -v docker-compose &> /dev/null && [ -f docker-compose.yml ]; then
    container_id=$(docker-compose ps -q unifi-mcp-server 2>/dev/null)
    if [ -n "$container_id" ]; then
        container_status=$(docker inspect --format='{{.State.Status}}' "$container_id" 2>/dev/null)
        if [ "$container_status" == "running" ]; then
            echo "Server is running in Docker"
            echo "Container ID: $container_id"
            echo "Container Status: $container_status"
            
            # Get the port mapping
            port_mapping=$(docker port "$container_id" 2>/dev/null | grep "8000/tcp" | cut -d":" -f2)
            if [ -n "$port_mapping" ]; then
                echo "Port mapping: $port_mapping"
                echo "Server URL: http://localhost:$port_mapping"
                
                # Check if the API is responding
                if command -v curl &> /dev/null; then
                    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port_mapping/docs)
                    if [ "$response" == "200" ]; then
                        echo "API is responding (HTTP 200 OK)"
                    else
                        echo "API is not responding properly (HTTP $response)"
                    fi
                fi
            else
                echo "Could not determine port mapping"
            fi
        else
            echo "Server container exists but is not running"
            echo "Container Status: $container_status"
        fi
    else
        echo "Server is not running in Docker"
    fi
fi

# Check Claude Desktop integration
if command -v python3 &> /dev/null && [ -f configure_claude.py ]; then
    echo "Checking Claude Desktop integration..."
    
    # Add --status option to configure_claude.py
    if ! grep -q "def check_status" configure_claude.py; then
        echo "Adding status check to configure_claude.py..."
        cat >> configure_claude.py << 'EOF'

def check_status(config_path):
    """Check if the Unifi MCP server is configured in Claude Desktop"""
    if not config_path:
        print("Could not find Claude Desktop config file.")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Could not read Claude Desktop config file.")
        return False
    
    if 'mcpServers' in config and 'unifi' in config['mcpServers']:
        print("Unifi MCP server is configured in Claude Desktop.")
        server_config = config['mcpServers']['unifi']
        print(f"Command: {server_config.get('command', 'N/A')}")
        print(f"Args: {server_config.get('args', [])}")
        return True
    else:
        print("Unifi MCP server is NOT configured in Claude Desktop.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        config_path = find_claude_config()
        check_status(config_path)
        sys.exit(0)
EOF
    fi
    
    python3 configure_claude.py --status
fi

echo "Status check complete."