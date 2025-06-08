#!/bin/bash
# Start the Unifi MCP Server

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
fi

# Check if UNIFI_API_KEY is set
if [ -z "$UNIFI_API_KEY" ]; then
    echo "Error: UNIFI_API_KEY environment variable is not set"
    echo "Please set it in your .env file or export it manually"
    exit 1
fi

# Check if Python virtual environment exists
if [ -d ".venv" ]; then
    echo "Activating Python virtual environment"
    source .venv/bin/activate
else
    echo "Warning: No virtual environment found (.venv directory missing)"
    echo "It's recommended to create a virtual environment:"
    echo "  uv venv"
    echo "  source .venv/bin/activate"
    echo "  uv sync"
    echo ""
    echo "Continuing without virtual environment..."
fi

# Start the server
echo "Starting Unifi MCP Server..."
python main.py
