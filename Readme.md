# Unifi MCP Server

A Model Context Protocol (MCP) server that integrates the UI.com Site Manager API with Claude Desktop, providing comprehensive access to UniFi network management through natural language.

## 🌟 Features

### Complete UI.com Site Manager API v1.0 Support
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

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- UniFi Site Manager API key
- Claude Desktop (for MCP integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Unimcp.git
   cd Unimcp
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your UniFi API key
   ```

4. **Run the server**
   ```bash
   ./start_server.sh  # On Windows: start_server.bat
   ```

### Claude Desktop Integration

Add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "unifi": {
      "command": "python3",
      "args": ["/path/to/Unimcp/main.py"],
      "env": {
        "UNIFI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 📖 Documentation

### Quick Links
- [📋 API Reference](docs/5_api_reference.md) - Complete API documentation
- [⚙️ Configuration Guide](docs/3_configuration_guide.md) - Setup and configuration
- [🐳 Docker Deployment](docs/6_docker_deployment.md) - Container deployment
- [🔧 Troubleshooting](docs/7_troubleshooting_guide.md) - Common issues and solutions

### Available Tools

#### Host Management
- `list_hosts` - List all hosts associated with your UI account
- `get_host_by_id` - Get detailed information about a specific host

#### Site Management
- `list_sites` - List all sites from hosts running UniFi Network applications

#### Device Management
- `list_devices` - List UniFi devices with filtering and pagination support

#### ISP Metrics
- `get_isp_metrics` - Retrieve ISP performance metrics (5m/1h intervals)
- `query_isp_metrics` - Query metrics with custom parameters

#### SD-WAN Management
- `list_sdwan_configs` - List all SD-WAN configurations
- `get_sdwan_config_by_id` - Get detailed SD-WAN configuration
- `get_sdwan_config_status` - Check SD-WAN configuration status

#### Legacy Tools (Backward Compatibility)
- `get_sites` - Legacy method for listing sites
- `get_devices` - Legacy method for listing devices
- `get_clients` - Legacy method (deprecated - not available in Site Manager API)

## 🔧 API Coverage

This implementation provides **100% coverage** of the UI.com Site Manager API v1.0 endpoints:

| Endpoint | Method | Status |
|----------|--------|--------|
| `/v1/hosts` | GET | ✅ Implemented |
| `/v1/hosts/{hostId}` | GET | ✅ Implemented |
| `/v1/sites` | GET | ✅ Implemented |
| `/v1/devices` | GET | ✅ Implemented |
| `/ea/isp-metrics/{type}` | GET | ✅ Implemented |
| `/ea/isp-metrics/query` | POST | ✅ Implemented |
| `/v1/sd-wan/configs` | GET | ✅ Implemented |
| `/v1/sd-wan/configs/{configId}` | GET | ✅ Implemented |
| `/v1/sd-wan/configs/{configId}/status` | GET | ✅ Implemented |

## 🐳 Docker Support

Run with Docker Compose:

```bash
docker-compose up -d
```

Or build and run manually:

```bash
docker build -t unifi-mcp-server .
docker run -p 8000:8000 -e UNIFI_API_KEY=your_key unifi-mcp-server
```

## 🔐 Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `UNIFI_API_KEY` | Yes | Your UniFi Site Manager API key | - |
| `UNIFI_API_URL` | No | UniFi API base URL | `https://api.ui.com` |

### Obtaining API Key

1. Log in to your UniFi console
2. Navigate to Settings → Control Plane → Integrations
3. Click "Create API Key"
4. Save the generated key securely

## 📊 Usage Examples

### With Claude Desktop

```
"Show me all my UniFi hosts"
"Get ISP metrics for the last 24 hours"
"List all devices with their status"
"Show SD-WAN configuration details for config_123"
```

### REST API

```bash
# List hosts
curl -X GET "http://localhost:8000/mcp/tools/list_hosts" \
  -H "Content-Type: application/json" \
  -d "{}"

# Get ISP metrics
curl -X GET "http://localhost:8000/mcp/tools/get_isp_metrics" \
  -H "Content-Type: application/json" \
  -d '{"metric_type": "5m", "duration": "24h"}'
```

## 🧪 Testing

Run the API coverage test:

```bash
source venv/bin/activate
python3 test_unifi_client.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [UI.com Site Manager API Documentation](https://developer.ui.com/site-manager-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)

## 📞 Support

- 📖 [Documentation](docs/README.md)
- 🐛 [Issue Tracker](https://github.com/your-username/Unimcp/issues)
- 💬 [Discussions](https://github.com/your-username/Unimcp/discussions)

