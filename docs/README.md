# Unifi MCP Server Documentation

Welcome to the documentation for the Unifi MCP Server, a Model Context Protocol (MCP) server that integrates with the Unifi Site Manager API, allowing you to interact with your Unifi network infrastructure using natural language through Claude Desktop.

## Table of Contents

1. [Project Overview](1_overview_project.md)
2. [Installation and Setup](2_installation_setup.md)
3. [Configuration Guide](3_configuration_guide.md)
4. [Usage Guide](4_usage_guide.md)
5. [API Reference](5_api_reference.md)
6. [Docker Deployment](6_docker_deployment.md)
7. [Troubleshooting Guide](7_troubleshooting_guide.md)
8. [Maintenance and Updates](8_maintenance_updates.md)

## Quick Start

1. **Install the MCP Server**:
   ```bash
   # Linux/macOS
   ./setup.sh
   
   # Windows
   setup.bat
   ```

2. **Configure your API Key**:
   Edit the `.env` file and add your Unifi API key:
   ```
   UNIFI_API_KEY=your_api_key_here
   ```

3. **Start the Server**:
   ```bash
   # Linux/macOS
   ./start_server.sh
   
   # Windows
   start_server.bat
   ```

4. **Configure Claude Desktop**:
   ```bash
   # Linux/macOS
   ./configure_claude.py
   
   # Windows
   python configure_claude.py
   ```

5. **Start Using Claude Desktop** with your Unifi network!

## Features

- **Natural Language Interface**: Interact with your Unifi network using conversational language
- **Site Management**: View and manage all your Unifi sites
- **Device Monitoring**: Get information about all devices in your network
- **Client Tracking**: Monitor clients connected to your network
- **Cross-Platform Support**: Works on Linux, macOS, and Windows
- **Docker Support**: Easy deployment using Docker containers
- **Secure Authentication**: Uses Unifi API keys for secure authentication

## System Requirements

- Python 3.8 or higher
- Unifi Site Manager API key
- Claude Desktop application

## Support and Feedback

If you encounter any issues or have suggestions for improvement, please check the [Troubleshooting Guide](7_troubleshooting_guide.md) or open an issue in the project repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.