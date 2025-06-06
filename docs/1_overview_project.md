# Unifi MCP Server - Project Overview

## Introduction

The Unifi MCP Server is a Model Context Protocol (MCP) server that integrates with the Unifi Site Manager API, allowing you to interact with your Unifi network infrastructure using natural language through Claude Desktop. This integration enables you to manage and monitor your Unifi devices, sites, and clients using simple conversational commands.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for AI assistants like Claude to interact with external tools and services. MCP servers expose functionality as "tools" that can be called by AI assistants, allowing them to perform actions in the real world based on natural language requests.

## Features

### Complete UI.com Site Manager API v1.0 Implementation
- **Host Management**: List and retrieve detailed information about UniFi hosts
- **Site Management**: Access all sites running UniFi Network applications
- **Device Management**: Monitor and manage UniFi devices across your network
- **ISP Metrics**: Retrieve performance metrics with customizable time ranges
- **SD-WAN Management**: Configure and monitor SD-WAN deployments

### MCP Integration
- **9 MCP Tools** covering all API endpoints
- **4 MCP Resources** for direct data access
- **Natural Language Interface** through Claude Desktop
- **Pagination Support** for large datasets
- **Error Handling** with comprehensive logging

### Enterprise Features
- **Cross-Platform Support**: Works on Linux, macOS, and Windows
- **Docker Support**: Easy deployment using Docker containers
- **Secure Authentication**: Uses UniFi API keys for secure authentication
- **Performance Monitoring**: Request timing and success rate tracking
- **Comprehensive Testing**: 100% API endpoint coverage verification

## Architecture

The Unifi MCP Server consists of the following components:

1. **FastAPI Backend**: A Python-based API server that handles requests from Claude Desktop
2. **MCP Integration**: Exposes Unifi API functionality as MCP tools
3. **Unifi API Client**: Communicates with the Unifi Site Manager API
4. **Claude Desktop Integration**: Configuration for Claude Desktop to access the MCP server

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Claude Desktop │────▶│  Unifi MCP      │────▶│  Unifi Site     │
│                 │     │  Server         │     │  Manager API    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Available Tools

The Unifi MCP Server exposes the following tools covering all UI.com Site Manager API v1.0 endpoints:

### Host Management
1. **list_hosts**: List all hosts associated with your UI account
2. **get_host_by_id**: Get detailed information about a specific host

### Site Management
3. **list_sites**: List all sites from hosts running UniFi Network applications

### Device Management
4. **list_devices**: List UniFi devices with filtering and pagination support

### ISP Metrics
5. **get_isp_metrics**: Retrieve ISP performance metrics (5m/1h intervals)
6. **query_isp_metrics**: Query metrics with custom parameters

### SD-WAN Management
7. **list_sdwan_configs**: List all SD-WAN configurations
8. **get_sdwan_config_by_id**: Get detailed SD-WAN configuration
9. **get_sdwan_config_status**: Check SD-WAN configuration status

### Legacy Tools (Backward Compatibility)
10. **get_sites**: Legacy method for listing sites
11. **get_devices**: Legacy method for listing devices
12. **get_clients**: Legacy method (deprecated - not available in Site Manager API)

### MCP Resources
- **unifi://hosts**: Direct access to host information
- **unifi://sites**: Direct access to sites data
- **unifi://devices**: Direct access to device information
- **unifi://sdwan-configs**: Direct access to SD-WAN configurations

## Prerequisites

- Python 3.8 or higher
- Unifi Site Manager API key
- Claude Desktop application

## Next Steps

- [Installation and Setup](2_installation_setup.md)
- [Configuration Guide](3_configuration_guide.md)
- [Usage Guide](4_usage_guide.md)
- [API Reference](5_api_reference.md)
- [Docker Deployment](6_docker_deployment.md)
- [Troubleshooting](7_troubleshooting_guide.md)
- [Maintenance and Updates](8_maintenance_updates.md)