# Configuration Guide

This guide explains how to configure both the Unifi MCP Server and Claude Desktop for optimal integration.

## Unifi MCP Server Configuration

### Environment Variables

The Unifi MCP Server uses environment variables for configuration. These can be set in the `.env` file or directly in your environment.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `UNIFI_API_KEY` | Yes | None | Your Unifi Site Manager API key |
| `UNIFI_API_URL` | No | `https://sitemanager.ui.com/api` | The base URL for the Unifi Site Manager API |

### The `.env` File

The `.env` file is the recommended way to configure the server. A template is provided in `.env.example`:

```
# Unifi API Key (required)
# Get this from Unifi console: Settings → Control Plane → Integrations → Create API Key
UNIFI_API_KEY=your_api_key_here

# Unifi API URL (optional, defaults to https://sitemanager.ui.com/api)
UNIFI_API_URL=https://sitemanager.ui.com/api
```

Copy this template to create your `.env` file:

```bash
cp .env.example .env
```

Then edit the `.env` file to add your actual API key.

## Claude Desktop Configuration

To use the Unifi MCP Server with Claude Desktop, you need to configure Claude Desktop to recognize and connect to your server.

### Automatic Configuration

The easiest way to configure Claude Desktop is to use the provided `configure_claude.py` script:

```bash
# Linux/macOS
./configure_claude.py

# Windows
python configure_claude.py
```

This script will:
1. Find the Claude Desktop configuration file on your system
2. Update it to include the Unifi MCP Server
3. Provide instructions for restarting Claude Desktop

### Manual Configuration

If the automatic configuration doesn't work, you can manually configure Claude Desktop:

1. Locate the Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Edit the configuration file to add the Unifi MCP Server:

   ```json
   {
     "mcpServers": {
       "unifi": {
         "command": "/path/to/uv",
         "args": [
           "--directory",
           "/path/to/unifi-mcp-server",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

   Replace `/path/to/uv` with the actual path to the `uv` executable (find it with `which uv` on Linux/macOS).
   Replace `/path/to/unifi-mcp-server` with the absolute path to your Unifi MCP Server directory.

   If you're using a virtual environment without `uv`, use this configuration instead:

   ```json
   {
     "mcpServers": {
       "unifi": {
         "command": "python",
         "args": [
           "/path/to/unifi-mcp-server/main.py"
         ]
       }
     }
   }
   ```

3. Save the configuration file and restart Claude Desktop.

### Verifying the Configuration

To verify that Claude Desktop is correctly configured:

1. Start the Unifi MCP Server:
   ```bash
   # Linux/macOS
   ./start_server.sh
   
   # Windows
   start_server.bat
   ```

2. Open Claude Desktop

3. Look for the Unifi tools in the Claude Desktop interface. You should see buttons or options for:
   - Get Sites
   - Get Devices
   - Get Clients

4. Try a simple query like "Show me all my Unifi sites"

## Advanced Configuration

### Server Port

By default, the server runs on port 8000. If you need to change this, modify the `main.py` file:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to your desired port
```

If you change the port, you'll also need to update the Docker configuration in `docker-compose.yml`:

```yaml
ports:
  - "8000:8000"  # Change both numbers to your desired port
```

### Logging

The server uses Python's built-in logging module. The default log level is `INFO`. To change the log level, modify the `main.py` file:

```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

### Docker Volume

When running with Docker, logs are stored in a volume. You can change the volume configuration in `docker-compose.yml`:

```yaml
volumes:
  - ./logs:/app/logs  # Change ./logs to your desired local directory
```

## Next Steps

After configuring the Unifi MCP Server and Claude Desktop:

1. Learn how to [use the MCP server](4_usage_guide.md) with Claude Desktop
2. Explore the [API Reference](5_api_reference.md) for more details on available tools
3. Check the [Troubleshooting Guide](7_troubleshooting_guide.md) if you encounter any issues