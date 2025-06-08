# Maintenance and Updates Guide

This guide provides information on how to maintain and update your Unifi MCP Server to ensure it continues to function correctly and securely.

## Table of Contents

- [Regular Maintenance Tasks](#regular-maintenance-tasks)
- [Updating the MCP Server](#updating-the-mcp-server)
- [Updating Dependencies](#updating-dependencies)
- [Updating the Unifi API Key](#updating-the-unifi-api-key)
- [Backup and Restore](#backup-and-restore)
- [Monitoring](#monitoring)
- [Security Considerations](#security-considerations)
- [Uninstalling](#uninstalling)

## Regular Maintenance Tasks

To keep your Unifi MCP Server running smoothly, perform these maintenance tasks regularly:

### Weekly Tasks

1. **Check for Updates**: Check for updates to the MCP server and its dependencies.
2. **Verify Server Status**: Ensure the server is running correctly.
3. **Review Logs**: Check logs for any errors or warnings.

### Monthly Tasks

1. **Update Dependencies**: Update Python dependencies to their latest versions.
2. **Test API Connection**: Run the test script to verify the connection to the Unifi API.
3. **Verify Claude Desktop Integration**: Ensure Claude Desktop can still connect to the server.

### Quarterly Tasks

1. **Renew API Key**: Generate a new Unifi API key for security.
2. **Review Security**: Check for any security advisories related to the dependencies.
3. **Full System Test**: Perform a complete test of all functionality.

## Updating the MCP Server

### Standard Installation

To update the MCP server:

1. Stop the server if it's running.
2. Pull the latest changes:
   ```bash
   git pull
   ```
3. Update dependencies:
   ```bash
   # Linux/macOS
   source .venv/bin/activate
   pip install -r requirements.txt
   
   # Windows
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Restart the server:
   ```bash
   # Linux/macOS
   ./start_server.sh
   
   # Windows
   start_server.bat
   ```

Alternatively, you can use the provided update scripts:

```bash
# Linux/macOS
./update.sh

# Windows
update.bat
```

### Docker Installation

To update the Docker installation:

1. Pull the latest changes:
   ```bash
   git pull
   ```
2. Rebuild and restart the container:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

## Updating Dependencies

Dependencies should be updated regularly to ensure security and compatibility.

### Standard Installation

To update dependencies:

1. Activate the virtual environment:
   ```bash
   # Linux/macOS
   source .venv/bin/activate
   
   # Windows
   .venv\Scripts\activate
   ```
2. Update all dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Test the server after updating dependencies.

### Docker Installation

Dependencies in the Docker container are updated when you rebuild the image:

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## Updating the Unifi API Key

It's good practice to periodically update your Unifi API key for security reasons.

1. Generate a new API key in the Unifi console:
   - Navigate to **Settings → Control Plane → Integrations**
   - Click on **Create API Key**
   - Copy the new API key

2. Update the `.env` file with the new API key:
   ```
   UNIFI_API_KEY=your_new_api_key_here
   ```

3. Restart the server to apply the changes:
   ```bash
   # Linux/macOS
   ./start_server.sh
   
   # Windows
   start_server.bat
   
   # Docker
   docker-compose restart
   ```

4. Test the connection with the new API key:
   ```bash
   # Standard installation
   python test_connection.py
   
   # Docker installation
   docker-compose exec unifi-mcp-server python test_connection.py
   ```

## Backup and Restore

### What to Backup

The most important files to backup are:

1. `.env` file (contains your API key)
2. Any custom modifications to the code
3. Logs (if you need to retain them)

### Backup Procedure

1. Create a backup of your `.env` file:
   ```bash
   cp .env .env.backup
   ```

2. If you've made custom modifications, create a backup of the entire project:
   ```bash
   # Linux/macOS
   tar -czvf unifi-mcp-server-backup.tar.gz --exclude=".venv" --exclude="__pycache__" .
   
   # Windows (using PowerShell)
   Compress-Archive -Path * -DestinationPath unifi-mcp-server-backup.zip -Force
   ```

### Restore Procedure

1. Restore your `.env` file:
   ```bash
   cp .env.backup .env
   ```

2. If you need to restore the entire project:
   ```bash
   # Linux/macOS
   tar -xzvf unifi-mcp-server-backup.tar.gz -C /path/to/restore
   
   # Windows (using PowerShell)
   Expand-Archive -Path unifi-mcp-server-backup.zip -DestinationPath /path/to/restore -Force
   ```

3. Reinstall dependencies:
   ```bash
   # Linux/macOS
   source .venv/bin/activate
   pip install -r requirements.txt
   
   # Windows
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Monitoring

### Checking Server Status

To check if the server is running:

```bash
# Linux/macOS
./status.sh

# Windows
status.bat

# Docker
docker-compose ps
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

### Monitoring Performance

To monitor the server's performance:

1. **CPU and Memory Usage**:
   ```bash
   # Linux/macOS
   ps aux | grep python
   
   # Windows
   tasklist | findstr python
   
   # Docker
   docker stats
   ```

2. **Network Usage**:
   ```bash
   # Linux
   nethogs
   
   # macOS
   nettop
   
   # Windows
   Resource Monitor > Network tab
   ```

## Security Considerations

### API Key Security

- Store your API key securely in the `.env` file
- Don't commit the `.env` file to version control
- Rotate your API key regularly
- Use the principle of least privilege when creating API keys

### Network Security

- Consider running the server behind a reverse proxy like Nginx or Traefik
- Use HTTPS if exposing the server to the internet
- Implement IP-based access controls if needed

### Docker Security

- Keep the Docker image updated
- Don't run the container as root
- Use Docker secrets for sensitive information
- Scan the container for vulnerabilities regularly

## Uninstalling

If you need to uninstall the Unifi MCP Server:

### Standard Installation

Use the provided uninstall scripts:

```bash
# Linux/macOS
./uninstall.sh

# Windows
uninstall.bat
```

These scripts will:
1. Stop the server if it's running
2. Remove the virtual environment
3. Remove any generated files
4. Preserve your `.env` file and logs

### Manual Uninstallation

If you prefer to uninstall manually:

1. Stop the server if it's running
2. Delete the virtual environment:
   ```bash
   rm -rf .venv
   ```
3. Remove any generated files:
   ```bash
   rm -rf __pycache__
   rm -rf logs
   ```

### Docker Uninstallation

To remove the Docker container and image:

```bash
# Stop and remove the container
docker-compose down

# Remove the image
docker rmi unifi-mcp-server

# Remove volumes (optional)
docker volume prune
```

## Next Steps

- Return to the [Project Overview](1_overview_project.md) for a high-level view of the project
- Check the [Troubleshooting Guide](7_troubleshooting_guide.md) if you encounter any issues
