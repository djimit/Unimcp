"""
MCP Tool definitions for UniFi API
"""
import logging
from fastapi import HTTPException

from .models import (
    ListHostsInput,
    ListHostsOutput,
    GetHostByIdInput,
    GetHostByIdOutput,
    ListSitesInput,
    ListSitesOutput,
    ListDevicesInput,
    ListDevicesOutput,
    GetIspMetricsInput,
    GetIspMetricsOutput,
    QueryIspMetricsInput,
    QueryIspMetricsOutput,
    ListSdwanConfigsInput,
    ListSdwanConfigsOutput,
    GetSdwanConfigByIdInput,
    GetSdwanConfigByIdOutput,
    GetSdwanConfigStatusInput,
    GetSdwanConfigStatusOutput,
    GetSitesInput,
    GetSitesOutput,
    GetDevicesInput,
    GetDevicesOutput,
    GetClientsInput,
    GetClientsOutput,
)

logger = logging.getLogger(__name__)


def register_tools(mcp_server, unifi_client):
    """Register all MCP tools with the server"""

    # Host Management Tools
    @mcp_server.tool(
        "list_hosts",
        ListHostsInput,
        ListHostsOutput,
        "Get a list of all hosts associated with the UI account",
    )
    async def list_hosts(input: ListHostsInput) -> ListHostsOutput:
        """Get a list of all hosts associated with the UI account"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.list_hosts(input.page_size, input.next_token)
            return ListHostsOutput(data=data)
        except Exception as e:
            logger.error(f"Error listing hosts: {e}")
            raise HTTPException(status_code=500, detail=f"Error listing hosts: {str(e)}")

    @mcp_server.tool(
        "get_host_by_id",
        GetHostByIdInput,
        GetHostByIdOutput,
        "Get detailed information about a specific host by ID",
    )
    async def get_host_by_id(input: GetHostByIdInput) -> GetHostByIdOutput:
        """Get detailed information about a specific host by ID"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.get_host_by_id(input.host_id)
            return GetHostByIdOutput(data=data)
        except Exception as e:
            logger.error(f"Error getting host by ID: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting host by ID: {str(e)}"
            )

    # Site Management Tools
    @mcp_server.tool(
        "list_sites",
        ListSitesInput,
        ListSitesOutput,
        "Get a list of all sites from hosts running the UniFi Network application",
    )
    async def list_sites(input: ListSitesInput) -> ListSitesOutput:
        """Get a list of all sites from hosts running the UniFi Network application"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.list_sites(input.page_size, input.next_token)
            return ListSitesOutput(data=data)
        except Exception as e:
            logger.error(f"Error listing sites: {e}")
            raise HTTPException(status_code=500, detail=f"Error listing sites: {str(e)}")

    # Device Management Tools
    @mcp_server.tool(
        "list_devices",
        ListDevicesInput,
        ListDevicesOutput,
        "Get a list of UniFi devices managed by hosts",
    )
    async def list_devices(input: ListDevicesInput) -> ListDevicesOutput:
        """Get a list of UniFi devices managed by hosts"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.list_devices(
                input.host_ids, input.time, input.page_size, input.next_token
            )
            return ListDevicesOutput(data=data)
        except Exception as e:
            logger.error(f"Error listing devices: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error listing devices: {str(e)}"
            )

    # ISP Metrics Tools
    @mcp_server.tool(
        "get_isp_metrics",
        GetIspMetricsInput,
        GetIspMetricsOutput,
        "Get ISP metrics data for all sites linked to the UI account's API key",
    )
    async def get_isp_metrics(input: GetIspMetricsInput) -> GetIspMetricsOutput:
        """Get ISP metrics data for all sites linked to the UI account's API key"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.get_isp_metrics(
                input.metric_type,
                input.begin_timestamp,
                input.end_timestamp,
                input.duration,
            )
            return GetIspMetricsOutput(data=data)
        except Exception as e:
            logger.error(f"Error getting ISP metrics: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting ISP metrics: {str(e)}"
            )

    @mcp_server.tool(
        "query_isp_metrics",
        QueryIspMetricsInput,
        QueryIspMetricsOutput,
        "Query ISP metrics data based on specific query parameters",
    )
    async def query_isp_metrics(input: QueryIspMetricsInput) -> QueryIspMetricsOutput:
        """Query ISP metrics data based on specific query parameters"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.query_isp_metrics(input.query_data)
            return QueryIspMetricsOutput(data=data)
        except Exception as e:
            logger.error(f"Error querying ISP metrics: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error querying ISP metrics: {str(e)}"
            )

    # SD-WAN Management Tools
    @mcp_server.tool(
        "list_sdwan_configs",
        ListSdwanConfigsInput,
        ListSdwanConfigsOutput,
        "Get a list of all SD-WAN configurations",
    )
    async def list_sdwan_configs(input: ListSdwanConfigsInput) -> ListSdwanConfigsOutput:
        """Get a list of all SD-WAN configurations"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.list_sdwan_configs(
                input.page_size, input.next_token
            )
            return ListSdwanConfigsOutput(data=data)
        except Exception as e:
            logger.error(f"Error listing SD-WAN configs: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error listing SD-WAN configs: {str(e)}"
            )

    @mcp_server.tool(
        "get_sdwan_config_by_id",
        GetSdwanConfigByIdInput,
        GetSdwanConfigByIdOutput,
        "Get detailed information about a specific SD-WAN configuration by ID",
    )
    async def get_sdwan_config_by_id(
        input: GetSdwanConfigByIdInput,
    ) -> GetSdwanConfigByIdOutput:
        """Get detailed information about a specific SD-WAN configuration by ID"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.get_sdwan_config_by_id(input.config_id)
            return GetSdwanConfigByIdOutput(data=data)
        except Exception as e:
            logger.error(f"Error getting SD-WAN config by ID: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting SD-WAN config by ID: {str(e)}"
            )

    @mcp_server.tool(
        "get_sdwan_config_status",
        GetSdwanConfigStatusInput,
        GetSdwanConfigStatusOutput,
        "Get the status of a specific SD-WAN configuration",
    )
    async def get_sdwan_config_status(
        input: GetSdwanConfigStatusInput,
    ) -> GetSdwanConfigStatusOutput:
        """Get the status of a specific SD-WAN configuration"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            data = await unifi_client.get_sdwan_config_status(input.config_id)
            return GetSdwanConfigStatusOutput(data=data)
        except Exception as e:
            logger.error(f"Error getting SD-WAN config status: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting SD-WAN config status: {str(e)}"
            )

    # Legacy Tools (for backward compatibility)
    @mcp_server.tool(
        "get_sites",
        GetSitesInput,
        GetSitesOutput,
        "Get a list of all Unifi sites (legacy method)",
    )
    async def get_sites(input: GetSitesInput) -> GetSitesOutput:
        """Get a list of all Unifi sites (legacy method)"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            sites = await unifi_client.get_sites()
            return GetSitesOutput(sites=sites)
        except Exception as e:
            logger.error(f"Error getting sites: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting sites: {str(e)}")

    @mcp_server.tool(
        "get_devices",
        GetDevicesInput,
        GetDevicesOutput,
        "Get a list of devices for a specific site (legacy method)",
    )
    async def get_devices(input: GetDevicesInput) -> GetDevicesOutput:
        """Get a list of devices for a specific site (legacy method)"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            devices = await unifi_client.get_devices(input.site_id)
            return GetDevicesOutput(devices=devices)
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting devices: {str(e)}"
            )

    @mcp_server.tool(
        "get_clients",
        GetClientsInput,
        GetClientsOutput,
        "Get a list of clients for a specific site (legacy method)",
    )
    async def get_clients(input: GetClientsInput) -> GetClientsOutput:
        """Get a list of clients for a specific site (legacy method)"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            clients = await unifi_client.get_clients(input.site_id)
            return GetClientsOutput(clients=clients)
        except Exception as e:
            logger.error(f"Error getting clients: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error getting clients: {str(e)}"
            )
