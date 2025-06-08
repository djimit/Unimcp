# Docker Deployment Guide

This guide explains how to deploy the Unifi MCP Server using Docker, which provides an isolated, consistent environment for running the server.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker Deployment Options](#docker-deployment-options)
- [Using Docker Compose](#using-docker-compose)
- [Using Docker CLI](#using-docker-cli)
- [Environment Variables](#environment-variables)
- [Volumes](#volumes)
- [Networking](#networking)
- [Docker Compose Configuration](#docker-compose-configuration)
- [Testing the Docker Deployment](#testing-the-docker-deployment)
- [Updating the Docker Deployment](#updating-the-docker-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying with Docker, ensure you have:

1. **Docker**: Install Docker on your system
   - [Docker Desktop for Windows/Mac](https://www.docker.com/products/docker-desktop)
   - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. **Docker Compose**: Usually included with Docker Desktop, or [install separately](https://docs.docker.com/compose/install/)

3. **Unifi API Key**: Obtain an API key from your Unifi console as described in the [Installation Guide](2_installation_setup.md#obtaining-a-unifi-api-key)

## Docker Deployment Options

You can deploy the Unifi MCP Server using Docker in two ways:

1. **Docker Compose** (recommended): Uses a YAML file to define and run the container
2. **Docker CLI**: Uses command-line instructions to build and run the container

## Using Docker Compose

Docker Compose is the recommended method for deploying the Unifi MCP Server.

### Step 1: Create the .env File

Create a `.env` file in the project directory with your Unifi API key:

```
UNIFI_API_KEY=your_api_key_here
UNIFI_API_URL=https://api.ui.com
```

### Step 2: Deploy with Docker Compose

Run the following command in the project directory:

```bash
docker-compose up -d
```

This command:
- Builds the Docker image if it doesn't exist
- Creates and starts the container in detached mode (-d)
- Sets up the environment variables from the .env file
- Maps port 8000 to your host
- Creates a volume for logs

### Step 3: Verify the Deployment

Check if the container is running:

```bash
docker-compose ps
```

You should see the `unifi-mcp-server` container running.

Access the OpenAPI documentation at:

```
http://localhost:8000/docs
```

## Using Docker CLI

If you prefer to use the Docker CLI directly, follow these steps:

### Step 1: Build the Docker Image

```bash
docker build -t unifi-mcp-server .
```

### Step 2: Run the Container

```bash
docker run -d \
  --name unifi-mcp-server \
  -p 8000:8000 \
  -e UNIFI_API_KEY=your_api_key_here \
  -e UNIFI_API_URL=https://api.ui.com \
  -v ./logs:/app/logs \
  unifi-mcp-server
```

Replace `your_api_key_here` with your actual Unifi API key.

### Step 3: Verify the Deployment

Check if the container is running:

```bash
docker ps
```

You should see the `unifi-mcp-server` container running.

Access the OpenAPI documentation at:

```
http://localhost:8000/docs
```

## Environment Variables

The Docker deployment supports the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `UNIFI_API_KEY` | Yes | None | Your Unifi Site Manager API key |
| `UNIFI_API_URL` | No | `https://api.ui.com` | The base URL for the Unifi Site Manager API |
| `PYTHONUNBUFFERED` | No | 1 | Ensures Python output is sent straight to the container log |

## Volumes

The Docker Compose configuration creates a volume for logs:

```yaml
volumes:
  - ./logs:/app/logs
```

This maps the `./logs` directory on your host to the `/app/logs` directory in the container, allowing you to access the logs even if the container is stopped or removed.

## Networking

The Docker Compose configuration maps port 8000 in the container to port 8000 on your host:

```yaml
ports:
  - "8000:8000"
```

If you need to use a different port on your host, change the first number:

```yaml
ports:
  - "9000:8000"  # Maps container port 8000 to host port 9000
```

## Docker Compose Configuration

The `docker-compose.yml` file defines the Docker deployment:

```yaml
version: '3'

services:
  unifi-mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - UNIFI_API_KEY=${UNIFI_API_KEY}
      - UNIFI_API_URL=${UNIFI_API_URL:-https://api.ui.com}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

Key components:
- `build: .`: Builds the image using the Dockerfile in the current directory
- `ports`: Maps container port 8000 to host port 8000
- `environment`: Sets environment variables from the .env file
- `restart: unless-stopped`: Automatically restarts the container if it crashes
- `volumes`: Maps the logs directory

## Testing the Docker Deployment

To test the Docker deployment, use the provided `docker_test.sh` script:

```bash
./docker_test.sh
```

This script:
1. Checks if the container is running
2. Executes the `test_connection.py` script inside the container
3. Reports the results

On Windows, you can run:

```bash
docker-compose exec unifi-mcp-server python test_connection.py
```

## Updating the Docker Deployment

To update the Docker deployment after making changes:

```bash
# Pull the latest code (if using Git)
git pull

# Rebuild and restart the container
docker-compose down
docker-compose build
docker-compose up -d
```

## Troubleshooting

### Container Fails to Start

If the container fails to start, check the logs:

```bash
docker-compose logs
```

Common issues:
- Missing or invalid `UNIFI_API_KEY`
- Network connectivity issues
- Port conflicts (another service using port 8000)

### API Connection Issues

If the container starts but can't connect to the Unifi API:

```bash
docker-compose exec unifi-mcp-server python test_connection.py
```

Common issues:
- Invalid API key
- Network connectivity issues
- Incorrect API URL

### Viewing Logs

To view the container logs:

```bash
# View all logs
docker-compose logs

# View only the most recent logs
docker-compose logs --tail=100

# Follow the logs (continuous output)
docker-compose logs -f
```

### Restarting the Container

If you need to restart the container:

```bash
docker-compose restart
```

### Rebuilding the Container

If you've made changes to the code or Dockerfile:

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## Next Steps

- Check the [Troubleshooting Guide](7_troubleshooting_guide.md) for more detailed troubleshooting steps
- Explore [Maintenance and Updates](8_maintenance_updates.md) for keeping your server up to date