#!/bin/bash
# Test the Unifi MCP Server Docker setup

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed or not in PATH"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found"
    echo "Creating a sample .env file from .env.example"
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env file and set your UNIFI_API_KEY"
    else
        echo "Error: .env.example file not found"
        exit 1
    fi
    
    exit 1
fi

# Check if UNIFI_API_KEY is set in .env
if ! grep -q "UNIFI_API_KEY" .env || grep -q "UNIFI_API_KEY=your_api_key_here" .env; then
    echo "Error: UNIFI_API_KEY not set in .env file"
    echo "Please edit .env file and set your UNIFI_API_KEY"
    exit 1
fi

# Build and start the Docker container
echo "Building and starting Docker container..."
docker-compose up --build -d

# Check if container is running
if [ $? -eq 0 ]; then
    echo "Docker container started successfully"
    echo "Testing API connection..."
    
    # Wait for the server to start
    sleep 5
    
    # Test the API connection
    response=$(curl -s http://localhost:8000/docs)
    
    if [ $? -eq 0 ] && [ ! -z "$response" ]; then
        echo "API connection successful!"
        echo "You can access the API documentation at http://localhost:8000/docs"
    else
        echo "Error: Could not connect to API"
        echo "Check the logs with: docker-compose logs"
    fi
else
    echo "Error: Failed to start Docker container"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi