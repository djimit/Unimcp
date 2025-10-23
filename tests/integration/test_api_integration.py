"""
Integration tests for full API workflow
"""
import pytest
from unittest.mock import AsyncMock, patch

from unifi_mcp.client import UnifiClient


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for API workflows"""

    @pytest.mark.asyncio
    async def test_full_host_workflow(
        self, mock_env, sample_host_data, mock_httpx_response
    ):
        """Test full workflow: list hosts -> get specific host"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_host_data)

            client = UnifiClient()

            # List all hosts
            hosts = await client.list_hosts()
            assert "data" in hosts
            assert len(hosts["data"]) > 0

            # Get specific host
            host_id = hosts["data"][0]["id"]
            host_detail = await client.get_host_by_id(host_id)
            assert "data" in host_detail

    @pytest.mark.asyncio
    async def test_pagination_workflow(
        self, mock_env, sample_host_data, mock_httpx_response
    ):
        """Test pagination workflow"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance

            # First page
            first_page = sample_host_data.copy()
            first_page["nextToken"] = "page2_token"
            mock_instance.request.return_value = mock_httpx_response(first_page)

            client = UnifiClient()
            page1 = await client.list_hosts(page_size=10)

            assert "nextToken" in page1
            assert page1["nextToken"] == "page2_token"

            # Second page
            second_page = sample_host_data.copy()
            second_page["nextToken"] = None
            mock_instance.request.return_value = mock_httpx_response(second_page)

            page2 = await client.list_hosts(page_size=10, next_token=page1["nextToken"])
            assert page2["nextToken"] is None

    @pytest.mark.asyncio
    async def test_metrics_query_workflow(
        self, mock_env, sample_isp_metrics_data, mock_httpx_response
    ):
        """Test ISP metrics query workflow"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_isp_metrics_data
            )

            client = UnifiClient()

            # Get metrics with different intervals
            metrics_5m = await client.get_isp_metrics("5m", duration="1h")
            assert "data" in metrics_5m

            metrics_1h = await client.get_isp_metrics("1h", duration="24h")
            assert "data" in metrics_1h

            # Query with custom parameters
            query_result = await client.query_isp_metrics(
                {"sites": ["site1"], "metrics": ["download", "upload"]}
            )
            assert "data" in query_result
