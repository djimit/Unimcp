# Installation and Setup Guide

This guide will walk you through the process of installing and setting up the Unifi MCP Server on your system.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+**: Required to run the MCP server
- **Unifi API Key**: Required to authenticate with the Unifi Site Manager API
- **Claude Desktop**: Required to interact with the MCP server using natural language

## Obtaining a Unifi API Key

To use the Unifi MCP Server, you need an API key from your Unifi console:

1. Log in to your Unifi console
2. Navigate to **Settings → Control Plane → Integrations**
3. Click on **Create API Key**
4. Copy the generated API key (it will look like `unifi_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
5. Store this key securely as you'll need it during setup

## Installation Methods

You can install the Unifi MCP Server using one of the following methods:

1. [Standard Installation](#standard-installation) (recommended for most users)
2. [Docker Installation](#docker-installation) (recommended for containerized environments)

## Standard Installation

### Linux and macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/unifi-mcp-server
   cd unifi-mcp-server
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

   This script will:
   - Check if Python is installed
   - Install `uv` package manager if not already installed
   - Create a Python virtual environment
   - Install all required dependencies
   - Create a `.env` file from the template
   - Make all scripts executable

3. Edit the `.env` file and set your Unifi API key:
   ```bash
   nano .env
   ```
   
   Update the following line:
   ```
   UNIFI_API_KEY=your_api_key_here
   ```

4. Test the connection to the Unifi API:
   ```bash
   ./test_connection.py
   ```

   If successful, you should see a list of your Unifi sites.

### Windows

1. Clone the repository:
   ```cmd
   git clone https://github.com/yourusername/unifi-mcp-server
   cd unifi-mcp-server
   ```

2. Run the setup script:
   ```cmd
   setup.bat
   ```

   This script will:
   - Check if Python is installed
   - Create a Python virtual environment
   - Install all required dependencies
   - Create a `.env` file from the template

3. Edit the `.env` file and set your Unifi API key:
   ```
   UNIFI_API_KEY=your_api_key_here
   ```

4. Test the connection to the Unifi API:
   ```cmd
   python test_connection.py
   ```

   If successful, you should see a list of your Unifi sites.

## Docker Installation

If you prefer to use Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/unifi-mcp-server
   cd unifi-mcp-server
   ```

2. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file and set your Unifi API key:
   ```bash
   nano .env
   ```
   
   Update the following line:
   ```
   UNIFI_API_KEY=your_api_key_here
   ```

4. Build and start the Docker container:
   ```bash
   docker-compose up -d
   ```

5. Test the Docker setup:
   ```bash
   ./docker_test.sh
   ```

   On Windows:
   ```cmd
   docker-compose exec unifi-mcp-server python test_connection.py
   ```

## Starting the Server

### Linux and macOS

To start the server:

```bash
./start_server.sh
```

### Windows

To start the server:

```cmd
start_server.bat
```

### Docker

If you're using Docker, the server should already be running after `docker-compose up -d`. You can check the status with:

```bash
docker-compose ps
```

## Verifying the Server

Once the server is running, you can verify it's working by accessing the OpenAPI documentation:

```
http://localhost:8000/docs
```

You should see the FastAPI Swagger UI with the available endpoints.

## Next Steps

After successfully installing and starting the server, proceed to:

1. [Configure Claude Desktop](3_configuration_guide.md) to connect to your MCP server
2. Learn how to [use the MCP server](4_usage_guide.md) with Claude Desktop

## Troubleshooting

If you encounter any issues during installation or setup, refer to the [Troubleshooting Guide](7_troubleshooting_guide.md).