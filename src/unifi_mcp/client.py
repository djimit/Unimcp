"""
UniFi API Client for Site Manager API
"""
import os
import logging
from typing import Dict, List, Any, Optional

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class UnifiClient:
    """Client for interacting with the Unifi Site Manager API"""

    def __init__(self) -> None:
        self.api_key = os.environ.get("UNIFI_API_KEY")
        if not self.api_key:
            logger.error("UNIFI_API_KEY environment variable not set")
            raise ValueError("UNIFI_API_KEY environment variable not set")

        self.base_url = os.environ.get("UNIFI_API_URL", "https://api.ui.com")
        self.headers = {"Accept": "application/json", "X-API-Key": self.api_key}
        logger.info(f"Initialized Unifi client with base URL: {self.base_url}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
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
                    timeout=30.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {e}")
                raise HTTPException(
                    status_code=500, detail=f"API request failed: {str(e)}"
                )
            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Unexpected error: {str(e)}"
                )

    # Host Management
    async def list_hosts(
        self, page_size: Optional[int] = None, next_token: Optional[str] = None
    ) -> Dict[str, Any]:
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
    async def list_sites(
        self, page_size: Optional[int] = None, next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of all sites from hosts running the UniFi Network application"""
        logger.info("Getting list of Unifi sites")
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if next_token:
            params["nextToken"] = next_token

        return await self._make_request("GET", "/v1/sites", params=params)

    # Device Management
    async def list_devices(
        self,
        host_ids: Optional[List[str]] = None,
        time: Optional[str] = None,
        page_size: Optional[int] = None,
        next_token: Optional[str] = None,
    ) -> Dict[str, Any]:
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
    async def get_isp_metrics(
        self,
        metric_type: str,
        begin_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        duration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get ISP metrics data for all sites linked to the UI account's API key"""
        logger.info(f"Getting ISP metrics for type: {metric_type}")
        params = {}
        if begin_timestamp:
            params["beginTimestamp"] = begin_timestamp
        if end_timestamp:
            params["endTimestamp"] = end_timestamp
        if duration:
            params["duration"] = duration

        return await self._make_request(
            "GET", f"/ea/isp-metrics/{metric_type}", params=params
        )

    async def query_isp_metrics(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Query ISP metrics data based on specific query parameters"""
        logger.info("Querying ISP metrics with custom parameters")
        return await self._make_request(
            "POST", "/ea/isp-metrics/query", json_data=query_data
        )

    # SD-WAN Management
    async def list_sdwan_configs(
        self, page_size: Optional[int] = None, next_token: Optional[str] = None
    ) -> Dict[str, Any]:
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
        return await self._make_request(
            "GET", f"/v1/sd-wan/configs/{config_id}/status"
        )

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
