#!/bin/bash
# Setup script for Unifi MCP Server

echo "Setting up Unifi MCP Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Warning: uv is not installed or not in PATH"
    echo "Would you like to install uv? (y/n)"
    read -r install_uv
    
    if [[ $install_uv =~ ^[Yy]$ ]]; then
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        
        # Add uv to PATH for this session
        export PATH="$HOME/.cargo/bin:$PATH"
    else
        echo "Continuing without uv. Will use pip instead."
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
if command -v uv &> /dev/null; then
    uv venv
    source .venv/bin/activate
    uv sync
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env file and set your UNIFI_API_KEY"
    else
        echo "Error: .env.example file not found"
        exit 1
    fi
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x start_server.sh
chmod +x docker_test.sh
chmod +x test_connection.py
chmod +x configure_claude.py

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and set your UNIFI_API_KEY"
echo "2. Run ./start_server.sh to start the server"
echo "3. Run ./configure_claude.py to configure Claude Desktop"
echo ""
echo "For Docker users:"
echo "1. Edit .env file and set your UNIFI_API_KEY"
echo "2. Run ./docker_test.sh to test the Docker setup"