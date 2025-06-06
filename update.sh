#!/bin/bash
# Update script for Unifi MCP Server

echo "Updating Unifi MCP Server..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed or not in PATH"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "Error: Not a git repository"
    echo "This script is intended to be run from a git repository"
    exit 1
fi

# Save current branch
current_branch=$(git symbolic-ref --short HEAD)

# Fetch latest changes
echo "Fetching latest changes..."
git fetch

# Check if there are any updates
local_rev=$(git rev-parse HEAD)
remote_rev=$(git rev-parse origin/$current_branch)

if [ "$local_rev" == "$remote_rev" ]; then
    echo "Already up to date"
    exit 0
fi

# Pull latest changes
echo "Pulling latest changes..."
git pull

# Check if requirements.txt has changed
if git diff --name-only HEAD@{1} HEAD | grep -q "requirements.txt"; then
    echo "requirements.txt has changed, updating dependencies..."
    
    # Update dependencies
    if command -v uv &> /dev/null; then
        source .venv/bin/activate
        uv sync
    else
        source .venv/bin/activate
        pip install -r requirements.txt
    fi
fi

echo "Update complete!"
echo ""
echo "You may need to restart the server for changes to take effect."