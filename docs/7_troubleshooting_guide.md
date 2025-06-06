# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Unifi MCP Server and its integration with Claude Desktop.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Connection Issues](#connection-issues)
- [API Key Issues](#api-key-issues)
- [Claude Desktop Integration Issues](#claude-desktop-integration-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)
- [Logging and Debugging](#logging-and-debugging)
- [Common Error Messages](#common-error-messages)

## Installation Issues

### Python Version Issues

**Problem**: Setup fails with Python version errors.

**Solution**:
1. Check your Python version:
   ```bash
   python --version
   ```
2. Ensure you have Python 3.8 or higher installed.
3. If needed, install a compatible Python version from [python.org](https://www.python.org/downloads/).

### Virtual Environment Issues

**Problem**: Virtual environment creation fails.

**Solution**:
1. Try creating the virtual environment manually:
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. If you encounter permission issues, try running with elevated privileges or check folder permissions.

### Dependency Installation Issues

**Problem**: Dependency installation fails.

**Solution**:
1. Update pip:
   ```bash
   pip install --upgrade pip
   ```
2. Install dependencies one by one to identify problematic packages:
   ```bash
   pip install fastapi
   pip install uvicorn
   # Continue with other dependencies
   ```
3. Check for conflicting dependencies in your environment.

## Configuration Issues

### Missing .env File

**Problem**: Server fails to start because it can't find environment variables.

**Solution**:
1. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file to add your Unifi API key.

### Invalid .env Format

**Problem**: Environment variables aren't being loaded correctly.

**Solution**:
1. Check the format of your `.env` file:
   ```
   UNIFI_API_KEY=your_api_key_here
   UNIFI_API_URL=https://sitemanager.ui.com/api
   ```
2. Ensure there are no spaces around the `=` sign.
3. Make sure there are no quotes around the values unless they're part of the value.

## Connection Issues

### Server Won't Start

**Problem**: The server fails to start.

**Solution**:
1. Check if another process is using port 8000:
   ```bash
   # Linux/macOS
   lsof -i :8000
   
   # Windows
   netstat -ano | findstr :8000
   ```
2. If the port is in use, either stop the other process or change the port in `main.py`.
3. Check the logs for specific error messages.

### Can't Access Server

**Problem**: The server is running but you can't access it in your browser.

**Solution**:
1. Verify the server is running:
   ```bash
   # Linux/macOS
   ps aux | grep python
   
   # Windows
   tasklist | findstr python
   ```
2. Try accessing with the IP address instead of localhost:
   ```
   http://127.0.0.1:8000/docs
   ```
3. Check if a firewall is blocking the connection.

### Connection Timeout

**Problem**: Requests to the Unifi API time out.

**Solution**:
1. Verify your internet connection.
2. Check if you can access the Unifi Site Manager API in a browser.
3. Verify the API URL in your `.env` file.
4. Try increasing the timeout in `test_connection.py`:
   ```python
   with httpx.Client(headers=headers, timeout=30.0) as client:  # Increase timeout
   ```

## API Key Issues

### Invalid API Key

**Problem**: The server reports "Invalid API key" or authentication errors.

**Solution**:
1. Verify your API key in the Unifi console.
2. Ensure the API key is correctly copied to your `.env` file without extra spaces or characters.
3. Generate a new API key if necessary.
4. Check if the API key has the necessary permissions.

### API Key Not Found

**Problem**: The server reports "UNIFI_API_KEY environment variable not set".

**Solution**:
1. Check if the `.env` file exists and contains the `UNIFI_API_KEY` variable.
2. If using Docker, ensure the environment variable is passed to the container.
3. Try setting the environment variable directly:
   ```bash
   # Linux/macOS
   export UNIFI_API_KEY=your_api_key_here
   
   # Windows
   set UNIFI_API_KEY=your_api_key_here
   ```

## Claude Desktop Integration Issues

### MCP Server Not Found

**Problem**: Claude Desktop can't find the MCP server.

**Solution**:
1. Verify the server is running.
2. Check the Claude Desktop configuration:
   ```bash
   python configure_claude.py
   ```
3. Restart Claude Desktop after making configuration changes.
4. Check if the paths in the Claude Desktop configuration are correct.

### Tool Not Available

**Problem**: The Unifi tools don't appear in Claude Desktop.

**Solution**:
1. Verify the server is running and accessible.
2. Check the Claude Desktop configuration.
3. Restart Claude Desktop.
4. Try restarting the MCP server.
5. Check the Claude Desktop logs for errors.

### Tool Execution Fails

**Problem**: Claude Desktop shows an error when trying to use a Unifi tool.

**Solution**:
1. Check if the server is running.
2. Verify the API key is valid.
3. Check the server logs for specific error messages.
4. Try restarting both the server and Claude Desktop.

## Docker Issues

### Container Won't Start

**Problem**: The Docker container fails to start.

**Solution**:
1. Check the Docker logs:
   ```bash
   docker-compose logs
   ```
2. Verify the environment variables are correctly set.
3. Check if the required ports are available.
4. Try rebuilding the container:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### Container Starts But Server Fails

**Problem**: The container starts but the server inside fails.

**Solution**:
1. Check the container logs:
   ```bash
   docker-compose logs
   ```
2. Verify the environment variables are correctly passed to the container.
3. Try running the test script inside the container:
   ```bash
   docker-compose exec unifi-mcp-server python test_connection.py
   ```

### Volume Mounting Issues

**Problem**: Logs aren't being saved to the host.

**Solution**:
1. Check the volume configuration in `docker-compose.yml`.
2. Verify the host directory exists and has the correct permissions.
3. Try using an absolute path for the volume:
   ```yaml
   volumes:
     - /absolute/path/to/logs:/app/logs
   ```

## Performance Issues

### Slow Response Times

**Problem**: The server takes a long time to respond to requests.

**Solution**:
1. Check your internet connection.
2. Verify the Unifi API is responsive.
3. Consider increasing the number of workers in `main.py`:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)  # Increase workers
   ```

### High CPU Usage

**Problem**: The server uses a lot of CPU resources.

**Solution**:
1. Check if there are many concurrent requests.
2. Consider limiting the number of workers.
3. Implement caching for frequently requested data.

## Logging and Debugging

### Enabling Debug Logs

To get more detailed logs, modify the logging configuration in `main.py`:

```python
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

### Viewing Logs

#### Standard Installation

Logs are printed to the console. You can redirect them to a file:

```bash
# Linux/macOS
./start_server.sh > server.log 2>&1

# Windows
start_server.bat > server.log 2>&1
```

#### Docker Installation

View logs with:

```bash
docker-compose logs

# Follow logs
docker-compose logs -f

# Show only recent logs
docker-compose logs --tail=100
```

### Testing API Connection

Use the `test_connection.py` script to test the connection to the Unifi API:

```bash
# Standard installation
python test_connection.py

# Docker installation
docker-compose exec unifi-mcp-server python test_connection.py
```

## Common Error Messages

### "UNIFI_API_KEY environment variable not set"

**Cause**: The server can't find the API key in the environment variables.

**Solution**:
1. Check if the `.env` file exists and contains the `UNIFI_API_KEY` variable.
2. Try setting the environment variable directly.
3. If using Docker, ensure the environment variable is passed to the container.

### "Connection failed with status code: 401"

**Cause**: The API key is invalid or has expired.

**Solution**:
1. Verify your API key in the Unifi console.
2. Generate a new API key if necessary.
3. Update the `.env` file with the new API key.

### "Connection failed with status code: 404"

**Cause**: The API endpoint doesn't exist or the URL is incorrect.

**Solution**:
1. Verify the API URL in your `.env` file.
2. Check if the Unifi Site Manager API has changed its endpoints.
3. Update the API URL if necessary.

### "Error connecting to Unifi API: ConnectTimeout"

**Cause**: The server can't connect to the Unifi API.

**Solution**:
1. Verify your internet connection.
2. Check if you can access the Unifi Site Manager API in a browser.
3. Verify the API URL in your `.env` file.
4. Try increasing the timeout in the client.

### "Could not find Claude Desktop config file"

**Cause**: The `configure_claude.py` script can't find the Claude Desktop configuration file.

**Solution**:
1. Verify Claude Desktop is installed.
2. Check if the configuration file exists in the expected location.
3. Manually create or edit the configuration file as described in the [Configuration Guide](3_configuration_guide.md).

## Next Steps

If you're still experiencing issues after trying the solutions in this guide:

1. Check the [Maintenance and Updates](8_maintenance_updates.md) guide for information on keeping your server up to date
2. Search for similar issues in the project's issue tracker
3. Consider reaching out to the community for help