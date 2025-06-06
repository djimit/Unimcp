#!/usr/bin/env python3
"""
Unifi MCP Server - Integrates Unifi Site Manager API with Claude Desktop
"""
import os
import logging
from typing import Dict, List, Any, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mcp import MCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("unifi-mcp-server")

# Initialize FastAPI app
app = FastAPI(title="Unifi MCP Server")

# Initialize MCP Server
mcp_server = MCPServer(
    name="unifi",
    description="MCP Server for Unifi Site Manager API integration",
    app=app,
)

# Unifi API client


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
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an HTTP request to the Unifi API"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json_data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {e}")
                raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    # Host Management
    async def list_hosts(self, page_size: Optional[int] = None, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all hosts associated with the UI account"""
        logger.info("Getting list of Unifi hosts")
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if next_token:
            params["nextToken"] = next_token
        
        return await self._make_request("GET", "/v1/hosts", params=params)
    
    async def get_host_by_id(self, host_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific host by ID"""
        logger.info(f"Getting host details for ID: {host_id}")
        return await self._make_request("GET", f"/v1/hosts/{host_id}")
    
    # Site Management
    async def list_sites(self, page_size: Optional[int] = None, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all sites from hosts running the UniFi Network application"""
        logger.info("Getting list of Unifi sites")
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if next_token:
            params["nextToken"] = next_token
        
        return await self._make_request("GET", "/v1/sites", params=params)
    
    # Device Management
    async def list_devices(self, host_ids: Optional[List[str]] = None, time: Optional[str] = None,
                          page_size: Optional[int] = None, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of UniFi devices managed by hosts"""
        logger.info("Getting list of Unifi devices")
        params = {}
        if host_ids:
            params["hostIds[]"] = host_ids
        if time:
            params["time"] = time
        if page_size:
            params["pageSize"] = page_size
        if next_token:
            params["nextToken"] = next_token
        
        return await self._make_request("GET", "/v1/devices", params=params)
    
    # ISP Metrics
    async def get_isp_metrics(self, metric_type: str, begin_timestamp: Optional[str] = None,
                             end_timestamp: Optional[str] = None, duration: Optional[str] = None) -> Dict[str, Any]:
        """Get ISP metrics data for all sites linked to the UI account's API key"""
        logger.info(f"Getting ISP metrics for type: {metric_type}")
        params = {}
        if begin_timestamp:
            params["beginTimestamp"] = begin_timestamp
        if end_timestamp:
            params["endTimestamp"] = end_timestamp
        if duration:
            params["duration"] = duration
        
        return await self._make_request("GET", f"/ea/isp-metrics/{metric_type}", params=params)
    
    async def query_isp_metrics(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Query ISP metrics data based on specific query parameters"""
        logger.info("Querying ISP metrics with custom parameters")
        return await self._make_request("POST", "/ea/isp-metrics/query", json_data=query_data)
    
    # SD-WAN Management
    async def list_sdwan_configs(self, page_size: Optional[int] = None, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get list of all SD-WAN configurations"""
        logger.info("Getting list of SD-WAN configurations")
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if next_token:
            params["nextToken"] = next_token
        
        return await self._make_request("GET", "/v1/sd-wan/configs", params=params)
    
    async def get_sdwan_config_by_id(self, config_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific SD-WAN configuration by ID"""
        logger.info(f"Getting SD-WAN config details for ID: {config_id}")
        return await self._make_request("GET", f"/v1/sd-wan/configs/{config_id}")
    
    async def get_sdwan_config_status(self, config_id: str) -> Dict[str, Any]:
        """Get the status of a specific SD-WAN configuration"""
        logger.info(f"Getting SD-WAN config status for ID: {config_id}")
        return await self._make_request("GET", f"/v1/sd-wan/configs/{config_id}/status")

    # Legacy methods for backward compatibility
    async def get_sites(self) -> List[Dict[str, Any]]:
        """Get list of all Unifi sites (legacy method)"""
        result = await self.list_sites()
        return result.get("data", [])
    
    async def get_devices(self, site_id: str) -> List[Dict[str, Any]]:
        """Get list of all devices for a specific site (legacy method)"""
        # Note: The new API doesn't filter by site_id directly, so we'll get all devices
        result = await self.list_devices()
        return result.get("data", [])
    
    async def get_clients(self, site_id: str) -> List[Dict[str, Any]]:
        """Get list of all clients for a specific site (legacy method)"""
        # Note: The Site Manager API doesn't have a direct clients endpoint
        # This would need to be implemented differently or removed
        logger.warning("get_clients method is not available in Site Manager API")
        return []


# Initialize Unifi client
unifi_client = None


@app.on_event("startup")
async def startup_event():
    global unifi_client
    try:
        unifi_client = UnifiClient()
        logger.info("Unifi client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Unifi client: {e}")
        # We'll continue running but tools will fail until the client is
        # properly
        # configured


# Define MCP Tool input/output models

# Host Management Models
class ListHostsInput(BaseModel):
    page_size: Optional[int] = Field(None, description="Number of items to return per page")
    next_token: Optional[str] = Field(None, description="Token for pagination to retrieve the next set of results")


class ListHostsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Host data from API response")


class GetHostByIdInput(BaseModel):
    host_id: str = Field(..., description="Unique identifier of the host")


class GetHostByIdOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Host details")


# Site Management Models
class ListSitesInput(BaseModel):
    page_size: Optional[int] = Field(None, description="Number of items to return per page")
    next_token: Optional[str] = Field(None, description="Token for pagination to retrieve the next set of results")


class ListSitesOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Sites data from API response")


# Device Management Models
class ListDevicesInput(BaseModel):
    host_ids: Optional[List[str]] = Field(None, description="List of host IDs to filter the results")
    time: Optional[str] = Field(None, description="Last processed timestamp of devices in RFC3339 format")
    page_size: Optional[int] = Field(None, description="Number of items to return per page")
    next_token: Optional[str] = Field(None, description="Token for pagination to retrieve the next set of results")


class ListDevicesOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Devices data from API response")


# ISP Metrics Models
class GetIspMetricsInput(BaseModel):
    metric_type: str = Field(..., description="Type of metrics (5m or 1h intervals)")
    begin_timestamp: Optional[str] = Field(None, description="The earliest timestamp to retrieve data from (RFC3339 format)")
    end_timestamp: Optional[str] = Field(None, description="The latest timestamp to retrieve data up to (RFC3339 format)")
    duration: Optional[str] = Field(None, description="Specifies the time range of metrics to retrieve")


class GetIspMetricsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="ISP metrics data")


class QueryIspMetricsInput(BaseModel):
    query_data: Dict[str, Any] = Field(..., description="Query parameters for ISP metrics")


class QueryIspMetricsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Queried ISP metrics data")


# SD-WAN Management Models
class ListSdwanConfigsInput(BaseModel):
    page_size: Optional[int] = Field(None, description="Number of items to return per page")
    next_token: Optional[str] = Field(None, description="Token for pagination to retrieve the next set of results")


class ListSdwanConfigsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="SD-WAN configurations data")


class GetSdwanConfigByIdInput(BaseModel):
    config_id: str = Field(..., description="Unique identifier of the SD-WAN configuration")


class GetSdwanConfigByIdOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="SD-WAN configuration details")


class GetSdwanConfigStatusInput(BaseModel):
    config_id: str = Field(..., description="Unique identifier of the SD-WAN configuration")


class GetSdwanConfigStatusOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="SD-WAN configuration status")


# Legacy Models (for backward compatibility)
class GetSitesInput(BaseModel):
    pass


class GetSitesOutput(BaseModel):
    sites: List[Dict[str, Any]] = Field(..., description="List of Unifi sites")


class GetDevicesInput(BaseModel):
    site_id: str = Field(..., description="ID of the site to get devices for")


class GetDevicesOutput(BaseModel):
    devices: List[Dict[str, Any]] = Field(
        ...,
        description="List of devices for the specified site"
    )


class GetClientsInput(BaseModel):
    site_id: str = Field(..., description="ID of the site to get clients for")


class GetClientsOutput(BaseModel):
    clients: List[Dict[str, Any]] = Field(
        ...,
        description="List of clients for the specified site"
    )


# Define MCP Tools

# Host Management Tools
@mcp_server.tool(
    "list_hosts",
    ListHostsInput,
    ListHostsOutput,
    "Get a list of all hosts associated with the UI account"
)
async def list_hosts(input: ListHostsInput) -> ListHostsOutput:
    """Get a list of all hosts associated with the UI account"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.list_hosts(input.page_size, input.next_token)
        return ListHostsOutput(data=data)
    except Exception as e:
        logger.error(f"Error listing hosts: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing hosts: {str(e)}"
        )


@mcp_server.tool(
    "get_host_by_id",
    GetHostByIdInput,
    GetHostByIdOutput,
    "Get detailed information about a specific host by ID"
)
async def get_host_by_id(input: GetHostByIdInput) -> GetHostByIdOutput:
    """Get detailed information about a specific host by ID"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.get_host_by_id(input.host_id)
        return GetHostByIdOutput(data=data)
    except Exception as e:
        logger.error(f"Error getting host by ID: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting host by ID: {str(e)}"
        )


# Site Management Tools
@mcp_server.tool(
    "list_sites",
    ListSitesInput,
    ListSitesOutput,
    "Get a list of all sites from hosts running the UniFi Network application"
)
async def list_sites(input: ListSitesInput) -> ListSitesOutput:
    """Get a list of all sites from hosts running the UniFi Network application"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.list_sites(input.page_size, input.next_token)
        return ListSitesOutput(data=data)
    except Exception as e:
        logger.error(f"Error listing sites: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing sites: {str(e)}"
        )


# Device Management Tools
@mcp_server.tool(
    "list_devices",
    ListDevicesInput,
    ListDevicesOutput,
    "Get a list of UniFi devices managed by hosts"
)
async def list_devices(input: ListDevicesInput) -> ListDevicesOutput:
    """Get a list of UniFi devices managed by hosts"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.list_devices(
            input.host_ids, input.time, input.page_size, input.next_token
        )
        return ListDevicesOutput(data=data)
    except Exception as e:
        logger.error(f"Error listing devices: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing devices: {str(e)}"
        )


# ISP Metrics Tools
@mcp_server.tool(
    "get_isp_metrics",
    GetIspMetricsInput,
    GetIspMetricsOutput,
    "Get ISP metrics data for all sites linked to the UI account's API key"
)
async def get_isp_metrics(input: GetIspMetricsInput) -> GetIspMetricsOutput:
    """Get ISP metrics data for all sites linked to the UI account's API key"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.get_isp_metrics(
            input.metric_type, input.begin_timestamp,
            input.end_timestamp, input.duration
        )
        return GetIspMetricsOutput(data=data)
    except Exception as e:
        logger.error(f"Error getting ISP metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting ISP metrics: {str(e)}"
        )


@mcp_server.tool(
    "query_isp_metrics",
    QueryIspMetricsInput,
    QueryIspMetricsOutput,
    "Query ISP metrics data based on specific query parameters"
)
async def query_isp_metrics(input: QueryIspMetricsInput) -> QueryIspMetricsOutput:
    """Query ISP metrics data based on specific query parameters"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.query_isp_metrics(input.query_data)
        return QueryIspMetricsOutput(data=data)
    except Exception as e:
        logger.error(f"Error querying ISP metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error querying ISP metrics: {str(e)}"
        )


# SD-WAN Management Tools
@mcp_server.tool(
    "list_sdwan_configs",
    ListSdwanConfigsInput,
    ListSdwanConfigsOutput,
    "Get a list of all SD-WAN configurations"
)
async def list_sdwan_configs(input: ListSdwanConfigsInput) -> ListSdwanConfigsOutput:
    """Get a list of all SD-WAN configurations"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.list_sdwan_configs(input.page_size, input.next_token)
        return ListSdwanConfigsOutput(data=data)
    except Exception as e:
        logger.error(f"Error listing SD-WAN configs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing SD-WAN configs: {str(e)}"
        )


@mcp_server.tool(
    "get_sdwan_config_by_id",
    GetSdwanConfigByIdInput,
    GetSdwanConfigByIdOutput,
    "Get detailed information about a specific SD-WAN configuration by ID"
)
async def get_sdwan_config_by_id(input: GetSdwanConfigByIdInput) -> GetSdwanConfigByIdOutput:
    """Get detailed information about a specific SD-WAN configuration by ID"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.get_sdwan_config_by_id(input.config_id)
        return GetSdwanConfigByIdOutput(data=data)
    except Exception as e:
        logger.error(f"Error getting SD-WAN config by ID: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting SD-WAN config by ID: {str(e)}"
        )


@mcp_server.tool(
    "get_sdwan_config_status",
    GetSdwanConfigStatusInput,
    GetSdwanConfigStatusOutput,
    "Get the status of a specific SD-WAN configuration"
)
async def get_sdwan_config_status(input: GetSdwanConfigStatusInput) -> GetSdwanConfigStatusOutput:
    """Get the status of a specific SD-WAN configuration"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        data = await unifi_client.get_sdwan_config_status(input.config_id)
        return GetSdwanConfigStatusOutput(data=data)
    except Exception as e:
        logger.error(f"Error getting SD-WAN config status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting SD-WAN config status: {str(e)}"
        )


# Legacy Tools (for backward compatibility)
@mcp_server.tool(
    "get_sites",
    GetSitesInput,
    GetSitesOutput,
    "Get a list of all Unifi sites (legacy method)"
)
async def get_sites(input: GetSitesInput) -> GetSitesOutput:
    """Get a list of all Unifi sites (legacy method)"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        sites = await unifi_client.get_sites()
        return GetSitesOutput(sites=sites)
    except Exception as e:
        logger.error(f"Error getting sites: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting sites: {str(e)}"
        )


@mcp_server.tool(
    "get_devices",
    GetDevicesInput,
    GetDevicesOutput,
    "Get a list of devices for a specific site (legacy method)"
)
async def get_devices(input: GetDevicesInput) -> GetDevicesOutput:
    """Get a list of devices for a specific site (legacy method)"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        devices = await unifi_client.get_devices(input.site_id)
        return GetDevicesOutput(devices=devices)
    except Exception as e:
        logger.error(f"Error getting devices: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting devices: {str(e)}"
        )


@mcp_server.tool(
    "get_clients",
    GetClientsInput,
    GetClientsOutput,
    "Get a list of clients for a specific site (legacy method)"
)
async def get_clients(input: GetClientsInput) -> GetClientsOutput:
    """Get a list of clients for a specific site (legacy method)"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        clients = await unifi_client.get_clients(input.site_id)
        return GetClientsOutput(clients=clients)
    except Exception as e:
        logger.error(f"Error getting clients: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting clients: {str(e)}"
        )


# Define MCP Resources
@mcp_server.resource("unifi://hosts")
async def resource_hosts():
    """Resource for accessing Unifi hosts"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        hosts = await unifi_client.list_hosts()
        return hosts
    except Exception as e:
        logger.error(f"Error accessing hosts resource: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing hosts resource: {str(e)}"
        )


@mcp_server.resource("unifi://sites")
async def resource_sites():
    """Resource for accessing Unifi sites"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        sites = await unifi_client.list_sites()
        return sites
    except Exception as e:
        logger.error(f"Error accessing sites resource: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing sites resource: {str(e)}"
        )


@mcp_server.resource("unifi://devices")
async def resource_devices():
    """Resource for accessing Unifi devices"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        devices = await unifi_client.list_devices()
        return devices
    except Exception as e:
        logger.error(f"Error accessing devices resource: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing devices resource: {str(e)}"
        )


@mcp_server.resource("unifi://sdwan-configs")
async def resource_sdwan_configs():
    """Resource for accessing SD-WAN configurations"""
    if not unifi_client:
        raise HTTPException(
            status_code=500,
            detail="Unifi client not initialized"
        )
    
    try:
        configs = await unifi_client.list_sdwan_configs()
        return configs
    except Exception as e:
        logger.error(f"Error accessing SD-WAN configs resource: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing SD-WAN configs resource: {str(e)}"
        )

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)