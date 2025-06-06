# API Reference

This document provides detailed information about the Unifi MCP Server's API endpoints, tools, and resources.

## Table of Contents

- [MCP Tools](#mcp-tools)
  - [Host Management](#host-management)
    - [list_hosts](#list_hosts)
    - [get_host_by_id](#get_host_by_id)
  - [Site Management](#site-management)
    - [list_sites](#list_sites)
    - [get_sites](#get_sites) (legacy)
  - [Device Management](#device-management)
    - [list_devices](#list_devices)
    - [get_devices](#get_devices) (legacy)
  - [ISP Metrics](#isp-metrics)
    - [get_isp_metrics](#get_isp_metrics)
    - [query_isp_metrics](#query_isp_metrics)
  - [SD-WAN Management](#sd-wan-management)
    - [list_sdwan_configs](#list_sdwan_configs)
    - [get_sdwan_config_by_id](#get_sdwan_config_by_id)
    - [get_sdwan_config_status](#get_sdwan_config_status)
  - [Legacy Tools](#legacy-tools)
    - [get_clients](#get_clients)
- [MCP Resources](#mcp-resources)
  - [unifi://hosts](#unifihosts)
  - [unifi://sites](#unifisites)
  - [unifi://devices](#unifidevices)
  - [unifi://sdwan-configs](#unifisdwan-configs)
- [REST API Endpoints](#rest-api-endpoints)
- [Data Models](#data-models)
  - [Host](#host)
  - [Site](#site)
  - [Device](#device)
  - [Client](#client)
  - [ISP Metrics](#isp-metrics-1)
  - [SD-WAN Configuration](#sd-wan-configuration)

## MCP Tools

MCP tools are functions that can be called by Claude Desktop to interact with your Unifi network. Each tool has a specific purpose, input parameters, and output format.

### Host Management

#### list_hosts

Retrieves a list of all hosts associated with the UI account making the API call.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page_size` | integer | No | Number of items to return per page |
| `next_token` | string | No | Token for pagination to retrieve the next set of results |

```json
{
  "page_size": 50,
  "next_token": "optional_pagination_token"
}
```

##### Output

Returns paginated data containing hosts information.

```json
{
  "data": {
    "hosts": [...],
    "nextToken": "next_page_token"
  }
}
```

##### Example Usage in Claude Desktop

```
Show me all my Unifi hosts
```

#### get_host_by_id

Retrieves detailed information about a specific host by ID.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `host_id` | string | Yes | Unique identifier of the host |

```json
{
  "host_id": "70A74197837ED00000000006797F060000"
}
```

##### Output

Returns detailed host information.

```json
{
  "data": {
    "id": "70A74197837ED00000000006797F060000",
    "hardwareId": "e5bf13cd-98a7-5a06-9463",
    "type": "ucore",
    "ipAddress": "220.130.137.169",
    "owner": true,
    "isBlocked": false,
    "registrationTime": "2024-04-15T09:30:29Z",
    "lastConnectionStateChange": "2024-04-15T09:30:29Z"
  }
}
```

##### Example Usage in Claude Desktop

```
Get details for host with ID 70A74197837ED00000000006797F060000
```

### Site Management

#### list_sites

Retrieves a list of all sites from hosts running the UniFi Network application.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page_size` | integer | No | Number of items to return per page |
| `next_token` | string | No | Token for pagination to retrieve the next set of results |

```json
{
  "page_size": 50,
  "next_token": "optional_pagination_token"
}
```

##### Output

Returns paginated data containing sites information.

```json
{
  "data": {
    "sites": [...],
    "nextToken": "next_page_token"
  }
}
```

##### Example Usage in Claude Desktop

```
List all my UniFi sites
```

### Device Management

#### list_devices

Retrieves a list of UniFi devices managed by hosts.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `host_ids` | array[string] | No | List of host IDs to filter the results |
| `time` | string | No | Last processed timestamp of devices in RFC3339 format |
| `page_size` | integer | No | Number of items to return per page |
| `next_token` | string | No | Token for pagination to retrieve the next set of results |

```json
{
  "host_ids": ["host1", "host2"],
  "time": "2024-04-15T09:30:29Z",
  "page_size": 50,
  "next_token": "optional_pagination_token"
}
```

##### Output

Returns paginated data containing devices information.

```json
{
  "data": {
    "devices": [...],
    "nextToken": "next_page_token"
  }
}
```

##### Example Usage in Claude Desktop

```
Show me all UniFi devices
```

### ISP Metrics

#### get_isp_metrics

Retrieves ISP metrics data for all sites linked to the UI account's API key.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `metric_type` | string | Yes | Type of metrics (5m or 1h intervals) |
| `begin_timestamp` | string | No | The earliest timestamp to retrieve data from (RFC3339 format) |
| `end_timestamp` | string | No | The latest timestamp to retrieve data up to (RFC3339 format) |
| `duration` | string | No | Specifies the time range of metrics to retrieve (24h for 5-minute metrics, 7d or 30d for 1-hour metrics) |

```json
{
  "metric_type": "5m",
  "begin_timestamp": "2024-04-15T09:30:29Z",
  "end_timestamp": "2024-04-16T09:30:29Z",
  "duration": "24h"
}
```

##### Output

Returns ISP metrics data.

```json
{
  "data": {
    "metrics": [...],
    "timestamp": "2024-04-15T09:30:29Z"
  }
}
```

##### Example Usage in Claude Desktop

```
Get 5-minute ISP metrics for the last 24 hours
```

#### query_isp_metrics

Query ISP metrics data based on specific query parameters.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query_data` | object | Yes | Query parameters for ISP metrics |

```json
{
  "query_data": {
    "sites": ["site1", "site2"],
    "metrics": ["download", "upload"],
    "timeRange": "1h"
  }
}
```

##### Output

Returns queried ISP metrics data.

```json
{
  "data": {
    "results": [...],
    "query": {...}
  }
}
```

##### Example Usage in Claude Desktop

```
Query ISP metrics for specific sites and metrics
```

### SD-WAN Management

#### list_sdwan_configs

Retrieves a list of all SD-WAN configurations associated with the UI account.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page_size` | integer | No | Number of items to return per page |
| `next_token` | string | No | Token for pagination to retrieve the next set of results |

```json
{
  "page_size": 50,
  "next_token": "optional_pagination_token"
}
```

##### Output

Returns paginated data containing SD-WAN configurations.

```json
{
  "data": {
    "configs": [...],
    "nextToken": "next_page_token"
  }
}
```

##### Example Usage in Claude Desktop

```
Show me all SD-WAN configurations
```

#### get_sdwan_config_by_id

Retrieves detailed information about a specific SD-WAN configuration by ID.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `config_id` | string | Yes | Unique identifier of the SD-WAN configuration |

```json
{
  "config_id": "config_123456"
}
```

##### Output

Returns detailed SD-WAN configuration information.

```json
{
  "data": {
    "id": "config_123456",
    "name": "Main Office SD-WAN",
    "status": "active",
    "deployment": {...}
  }
}
```

##### Example Usage in Claude Desktop

```
Get details for SD-WAN config with ID config_123456
```

#### get_sdwan_config_status

Retrieves the status of a specific SD-WAN configuration.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `config_id` | string | Yes | Unique identifier of the SD-WAN configuration |

```json
{
  "config_id": "config_123456"
}
```

##### Output

Returns SD-WAN configuration status.

```json
{
  "data": {
    "configId": "config_123456",
    "status": "deployed",
    "lastUpdated": "2024-04-15T09:30:29Z",
    "errors": [],
    "associatedHubs": [...]
  }
}
```

##### Example Usage in Claude Desktop

```
Check status of SD-WAN config config_123456
```

### Legacy Tools

These tools are maintained for backward compatibility but it's recommended to use the newer equivalent tools.

#### get_sites

*Legacy method* - Use `list_sites` instead for new implementations.

Retrieves a list of all Unifi sites accessible with your API key.

##### Input

No input parameters required.

```json
{}
```

##### Output

Returns a list of sites with their IDs and names.

```json
{
  "sites": [
    {
      "id": "site1",
      "name": "Main Office"
    },
    {
      "id": "site2",
      "name": "Branch Office"
    }
  ]
}
```

##### Example Usage in Claude Desktop

```
Show me all my Unifi sites
```

#### get_devices

*Legacy method* - Use `list_devices` instead for new implementations.

Retrieves a list of all devices for a specific site.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | The ID of the site to get devices for |

```json
{
  "site_id": "site1"
}
```

##### Output

Returns a list of devices with their details.

```json
{
  "devices": [
    {
      "id": "device1",
      "name": "AP-Office",
      "type": "UAP-AC-Pro",
      "status": "connected"
    },
    {
      "id": "device2",
      "name": "Switch-Main",
      "type": "USW-Pro-24-PoE",
      "status": "connected"
    }
  ]
}
```

##### Example Usage in Claude Desktop

```
Show me all devices at my Main Office site
```

#### get_clients

*Note: This method is deprecated* - The Site Manager API doesn't provide a direct clients endpoint.

Retrieves a list of all clients connected to a specific Unifi site.

##### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | The ID of the site to get clients for |

```json
{
  "site_id": "site1"
}
```

##### Output

Returns an empty list as this functionality is not available in the Site Manager API.

```json
{
  "clients": []
}
```

##### Example Usage in Claude Desktop

```
Show me all clients connected to my Main Office site
```

## MCP Resources

MCP resources are data sources that can be accessed by Claude Desktop. They provide a way to retrieve information without explicitly calling a tool.

### unifi://hosts

Resource for accessing Unifi hosts.

#### Output

Returns hosts data from the API.

```json
{
  "data": [
    {
      "id": "70A74197837ED00000000006797F060000",
      "hardwareId": "e5bf13cd-98a7-5a06-9463",
      "type": "ucore",
      "ipAddress": "220.130.137.169",
      "owner": true,
      "isBlocked": false,
      "registrationTime": "2024-04-15T09:30:29Z",
      "lastConnectionStateChange": "2024-04-15T09:30:29Z"
    }
  ]
}
```

### unifi://sites

Resource for accessing Unifi sites.

#### Output

Returns sites data from the API.

```json
{
  "data": [
    {
      "id": "site1",
      "name": "Main Office",
      "meta": {...},
      "statistics": {...}
    },
    {
      "id": "site2",
      "name": "Branch Office",
      "meta": {...},
      "statistics": {...}
    }
  ]
}
```

### unifi://devices

Resource for accessing Unifi devices.

#### Output

Returns devices data from the API.

```json
{
  "data": [
    {
      "id": "device1",
      "name": "AP-Office",
      "type": "UAP-AC-Pro",
      "status": "connected",
      "devices": {...}
    },
    {
      "id": "device2",
      "name": "Switch-Main",
      "type": "USW-Pro-24-PoE",
      "status": "connected",
      "devices": {...}
    }
  ]
}
```

### unifi://sdwan-configs

Resource for accessing SD-WAN configurations.

#### Output

Returns SD-WAN configurations data from the API.

```json
{
  "data": [
    {
      "id": "config_123456",
      "name": "Main Office SD-WAN",
      "status": "active",
      "deployment": {...}
    }
  ]
}
```

## REST API Endpoints

The Unifi MCP Server exposes the following REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | OpenAPI documentation |
| `/openapi.json` | GET | OpenAPI specification |
| `/mcp/tools` | GET | List of available MCP tools |
| `/mcp/tools/{tool_name}` | POST | Execute an MCP tool |
| `/mcp/resources/{resource_uri}` | GET | Access an MCP resource |

## Data Models

### Host

Represents a Unifi host device.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the host device |
| `hardwareId` | string | Hardware identifier of the device |
| `type` | string | Type of the device (console, network-server) |
| `ipAddress` | string | Current IP address of the device |
| `owner` | boolean | Indicates if the current user is the owner of this device |
| `isBlocked` | boolean | Indicates if the device is blocked from cloud access |
| `registrationTime` | string | Time in RFC3339 format when the device was registered to the cloud |
| `lastConnectionStateChange` | string | Time in RFC3339 format when the connection state last changed |
| `latestBackupTime` | string | Time in RFC3339 format of the latest device backup |
| `userData` | object | User-specific data associated with the device including permissions and role information |

### Site

Represents a Unifi site.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the site |
| `name` | string | Human-readable name of the site |
| `meta` | object | Metadata associated with the site |
| `statistics` | object | Statistical data for the site |

### Device

Represents a Unifi device.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the device |
| `name` | string | Name of the device |
| `type` | string | Type/model of the device |
| `status` | string | Current status (e.g., "connected", "disconnected") |
| `devices` | object | Additional device-specific data |

### Client

Represents a client connected to a Unifi network.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the client |
| `name` | string | Name of the client |
| `ip` | string | IP address of the client |
| `mac` | string | MAC address of the client |

### ISP Metrics

Represents ISP performance metrics data.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | Time of the metric in RFC3339 format |
| `download` | number | Download speed in Mbps |
| `upload` | number | Upload speed in Mbps |
| `latency` | number | Latency in milliseconds |
| `jitter` | number | Jitter in milliseconds |
| `packetLoss` | number | Packet loss percentage |
| `siteId` | string | Site identifier where the metric was collected |

### SD-WAN Configuration

Represents an SD-WAN configuration.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the SD-WAN configuration |
| `name` | string | Name of the configuration |
| `status` | string | Current status of the configuration |
| `deployment` | object | Deployment details and settings |
| `lastUpdated` | string | Time in RFC3339 format when the configuration was last updated |
| `errors` | array | List of configuration errors if any |
| `associatedHubs` | array | List of hubs associated with this configuration |

## Implementation Details

### UnifiClient Class

The `UnifiClient` class handles communication with the Unifi Site Manager API. It provides methods for all API endpoints including host management, site management, device management, ISP metrics, and SD-WAN configurations.

```python
class UnifiClient:
    """Client for interacting with the Unifi Site Manager API"""
    
    def __init__(self):
        self.api_key = os.environ.get("UNIFI_API_KEY")
        if not self.api_key:
            logger.error("UNIFI_API_KEY environment variable not set")
            raise ValueError("UNIFI_API_KEY environment variable not set")
        
        self.base_url = os.environ.get(
            "UNIFI_API_URL",
            "https://api.ui.com"
        )
        self.headers = {
            "Accept": "application/json",
            "X-API-Key": self.api_key
        }
        logger.info(f"Initialized Unifi client with base URL: {self.base_url}")
    
    async def _make_request(self, method: str, endpoint: str,
                           params: Optional[Dict] = None,
                           json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an HTTP request to the Unifi API"""
        # HTTP client implementation with error handling...
    
    # Host Management
    async def list_hosts(self, page_size: Optional[int] = None,
                        next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all hosts associated with the UI account"""
    
    async def get_host_by_id(self, host_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific host by ID"""
    
    # Site Management
    async def list_sites(self, page_size: Optional[int] = None,
                        next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all sites from hosts running the UniFi Network application"""
    
    # Device Management
    async def list_devices(self, host_ids: Optional[List[str]] = None,
                          time: Optional[str] = None,
                          page_size: Optional[int] = None,
                          next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of UniFi devices managed by hosts"""
    
    # ISP Metrics
    async def get_isp_metrics(self, metric_type: str,
                             begin_timestamp: Optional[str] = None,
                             end_timestamp: Optional[str] = None,
                             duration: Optional[str] = None) -> Dict[str, Any]:
        """Get ISP metrics data for all sites linked to the UI account's API key"""
    
    async def query_isp_metrics(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Query ISP metrics data based on specific query parameters"""
    
    # SD-WAN Management
    async def list_sdwan_configs(self, page_size: Optional[int] = None,
                                next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all SD-WAN configurations"""
    
    async def get_sdwan_config_by_id(self, config_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific SD-WAN configuration by ID"""
    
    async def get_sdwan_config_status(self, config_id: str) -> Dict[str, Any]:
        """Get the status of a specific SD-WAN configuration"""
    
    # Legacy methods for backward compatibility
    async def get_sites(self) -> List[Dict[str, Any]]:
        """Get list of all Unifi sites (legacy method)"""
    
    async def get_devices(self, site_id: str) -> List[Dict[str, Any]]:
        """Get list of all devices for a specific site (legacy method)"""
    
    async def get_clients(self, site_id: str) -> List[Dict[str, Any]]:
        """Get list of all clients for a specific site (legacy method)"""
```

### MCP Tool Definitions

MCP tools are defined using the `@mcp_server.tool` decorator, which specifies the tool name, input model, output model, and description.

```python
@mcp_server.tool(
    "get_sites",
    GetSitesInput,
    GetSitesOutput,
    "Get a list of all Unifi sites"
)
async def get_sites(input: GetSitesInput) -> GetSitesOutput:
    """Get a list of all Unifi sites"""
    # Implementation details...
```

## Error Handling

The Unifi MCP Server handles errors in the following ways:

1. **Client Initialization Errors**: If the Unifi API key is not set, the server will log an error but continue running. Tools will fail until the client is properly configured.

2. **Tool Execution Errors**: If an error occurs during tool execution, the server will return an HTTP 500 error with details about the error.

3. **Resource Access Errors**: If an error occurs when accessing a resource, the server will return an HTTP 500 error with details about the error.

## Next Steps

- Learn about [Docker Deployment](6_docker_deployment.md) for containerized environments
- Check the [Troubleshooting Guide](7_troubleshooting_guide.md) if you encounter any issues
- Explore [Maintenance and Updates](8_maintenance_updates.md) for keeping your server up to date