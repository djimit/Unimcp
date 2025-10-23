"""
MCP Resource definitions for UniFi API
"""
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def register_resources(mcp_server, unifi_client):
    """Register all MCP resources with the server"""

    @mcp_server.resource("unifi://hosts")
    async def resource_hosts():
        """Resource for accessing Unifi hosts"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            hosts = await unifi_client.list_hosts()
            return hosts
        except Exception as e:
            logger.error(f"Error accessing hosts resource: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error accessing hosts resource: {str(e)}"
            )

    @mcp_server.resource("unifi://sites")
    async def resource_sites():
        """Resource for accessing Unifi sites"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            sites = await unifi_client.list_sites()
            return sites
        except Exception as e:
            logger.error(f"Error accessing sites resource: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error accessing sites resource: {str(e)}"
            )

    @mcp_server.resource("unifi://devices")
    async def resource_devices():
        """Resource for accessing Unifi devices"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            devices = await unifi_client.list_devices()
            return devices
        except Exception as e:
            logger.error(f"Error accessing devices resource: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error accessing devices resource: {str(e)}"
            )

    @mcp_server.resource("unifi://sdwan-configs")
    async def resource_sdwan_configs():
        """Resource for accessing SD-WAN configurations"""
        if not unifi_client:
            raise HTTPException(status_code=500, detail="Unifi client not initialized")

        try:
            configs = await unifi_client.list_sdwan_configs()
            return configs
        except Exception as e:
            logger.error(f"Error accessing SD-WAN configs resource: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error accessing SD-WAN configs resource: {str(e)}",
            )
