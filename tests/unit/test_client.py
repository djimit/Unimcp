"""
Unit tests for UnifiClient
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from unifi_mcp.client import UnifiClient


@pytest.mark.unit
class TestUnifiClientInit:
    """Test UnifiClient initialization"""

    def test_init_success(self, mock_env):
        """Test successful initialization with API key"""
        client = UnifiClient()
        assert client.api_key == "test_api_key_12345"
        assert client.base_url == "https://api.ui.com"
        assert "X-API-Key" in client.headers

    def test_init_missing_api_key(self, monkeypatch):
        """Test initialization fails without API key"""
        monkeypatch.delenv("UNIFI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="UNIFI_API_KEY environment variable not set"):
            UnifiClient()

    def test_init_custom_url(self, monkeypatch):
        """Test initialization with custom API URL"""
        monkeypatch.setenv("UNIFI_API_KEY", "test_key")
        monkeypatch.setenv("UNIFI_API_URL", "https://custom.api.com")
        client = UnifiClient()
        assert client.base_url == "https://custom.api.com"


@pytest.mark.unit
class TestUnifiClientHostManagement:
    """Test host management methods"""

    @pytest.mark.asyncio
    async def test_list_hosts_success(
        self, unifi_client, sample_host_data, mock_httpx_response
    ):
        """Test successful hosts listing"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_host_data)

            result = await unifi_client.list_hosts()

            assert result == sample_host_data
            mock_instance.request.assert_called_once()
            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/v1/hosts"
            assert call_args[1]["method"] == "GET"

    @pytest.mark.asyncio
    async def test_list_hosts_with_pagination(
        self, unifi_client, sample_host_data, mock_httpx_response
    ):
        """Test hosts listing with pagination parameters"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_host_data)

            result = await unifi_client.list_hosts(page_size=50, next_token="token123")

            mock_instance.request.assert_called_once()
            call_args = mock_instance.request.call_args
            assert call_args[1]["params"]["pageSize"] == 50
            assert call_args[1]["params"]["nextToken"] == "token123"

    @pytest.mark.asyncio
    async def test_get_host_by_id_success(
        self, unifi_client, sample_host_data, mock_httpx_response
    ):
        """Test successful get host by ID"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_host_data)

            result = await unifi_client.get_host_by_id("host_123")

            assert result == sample_host_data
            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/v1/hosts/host_123"


@pytest.mark.unit
class TestUnifiClientSiteManagement:
    """Test site management methods"""

    @pytest.mark.asyncio
    async def test_list_sites_success(
        self, unifi_client, sample_site_data, mock_httpx_response
    ):
        """Test successful sites listing"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_site_data)

            result = await unifi_client.list_sites()

            assert result == sample_site_data
            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/v1/sites"


@pytest.mark.unit
class TestUnifiClientDeviceManagement:
    """Test device management methods"""

    @pytest.mark.asyncio
    async def test_list_devices_success(
        self, unifi_client, sample_device_data, mock_httpx_response
    ):
        """Test successful devices listing"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_device_data)

            result = await unifi_client.list_devices()

            assert result == sample_device_data

    @pytest.mark.asyncio
    async def test_list_devices_with_filters(
        self, unifi_client, sample_device_data, mock_httpx_response
    ):
        """Test devices listing with filters"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_device_data)

            result = await unifi_client.list_devices(
                host_ids=["host1", "host2"],
                time="2025-01-01T00:00:00Z",
                page_size=25,
                next_token="token456",
            )

            call_args = mock_instance.request.call_args
            params = call_args[1]["params"]
            assert params["hostIds[]"] == ["host1", "host2"]
            assert params["time"] == "2025-01-01T00:00:00Z"
            assert params["pageSize"] == 25
            assert params["nextToken"] == "token456"


@pytest.mark.unit
class TestUnifiClientISPMetrics:
    """Test ISP metrics methods"""

    @pytest.mark.asyncio
    async def test_get_isp_metrics_success(
        self, unifi_client, sample_isp_metrics_data, mock_httpx_response
    ):
        """Test successful ISP metrics retrieval"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_isp_metrics_data
            )

            result = await unifi_client.get_isp_metrics("5m")

            assert result == sample_isp_metrics_data
            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/ea/isp-metrics/5m"

    @pytest.mark.asyncio
    async def test_get_isp_metrics_with_timerange(
        self, unifi_client, sample_isp_metrics_data, mock_httpx_response
    ):
        """Test ISP metrics with time range parameters"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_isp_metrics_data
            )

            result = await unifi_client.get_isp_metrics(
                "1h",
                begin_timestamp="2025-01-01T00:00:00Z",
                end_timestamp="2025-01-02T00:00:00Z",
                duration="24h",
            )

            call_args = mock_instance.request.call_args
            params = call_args[1]["params"]
            assert params["beginTimestamp"] == "2025-01-01T00:00:00Z"
            assert params["endTimestamp"] == "2025-01-02T00:00:00Z"
            assert params["duration"] == "24h"

    @pytest.mark.asyncio
    async def test_query_isp_metrics_success(
        self, unifi_client, sample_isp_metrics_data, mock_httpx_response
    ):
        """Test ISP metrics query"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_isp_metrics_data
            )

            query_data = {"sites": ["site1", "site2"], "metrics": ["download", "upload"]}
            result = await unifi_client.query_isp_metrics(query_data)

            call_args = mock_instance.request.call_args
            assert call_args[1]["json"] == query_data
            assert call_args[1]["method"] == "POST"


@pytest.mark.unit
class TestUnifiClientSDWAN:
    """Test SD-WAN management methods"""

    @pytest.mark.asyncio
    async def test_list_sdwan_configs_success(
        self, unifi_client, sample_sdwan_config_data, mock_httpx_response
    ):
        """Test successful SD-WAN configs listing"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_sdwan_config_data
            )

            result = await unifi_client.list_sdwan_configs()

            assert result == sample_sdwan_config_data
            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/v1/sd-wan/configs"

    @pytest.mark.asyncio
    async def test_get_sdwan_config_by_id_success(
        self, unifi_client, sample_sdwan_config_data, mock_httpx_response
    ):
        """Test successful get SD-WAN config by ID"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_sdwan_config_data
            )

            result = await unifi_client.get_sdwan_config_by_id("config_123")

            call_args = mock_instance.request.call_args
            assert call_args[1]["url"] == "https://api.ui.com/v1/sd-wan/configs/config_123"

    @pytest.mark.asyncio
    async def test_get_sdwan_config_status_success(
        self, unifi_client, sample_sdwan_config_data, mock_httpx_response
    ):
        """Test successful get SD-WAN config status"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(
                sample_sdwan_config_data
            )

            result = await unifi_client.get_sdwan_config_status("config_123")

            call_args = mock_instance.request.call_args
            assert (
                call_args[1]["url"]
                == "https://api.ui.com/v1/sd-wan/configs/config_123/status"
            )


@pytest.mark.unit
class TestUnifiClientLegacyMethods:
    """Test legacy backward compatibility methods"""

    @pytest.mark.asyncio
    async def test_get_sites_legacy(
        self, unifi_client, sample_site_data, mock_httpx_response
    ):
        """Test legacy get_sites method"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_site_data)

            result = await unifi_client.get_sites()

            assert result == sample_site_data["data"]

    @pytest.mark.asyncio
    async def test_get_devices_legacy(
        self, unifi_client, sample_device_data, mock_httpx_response
    ):
        """Test legacy get_devices method"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.return_value = mock_httpx_response(sample_device_data)

            result = await unifi_client.get_devices("site_123")

            assert result == sample_device_data["data"]

    @pytest.mark.asyncio
    async def test_get_clients_legacy(self, unifi_client):
        """Test legacy get_clients method (not available in API)"""
        result = await unifi_client.get_clients("site_123")
        assert result == []


@pytest.mark.unit
class TestUnifiClientErrorHandling:
    """Test error handling"""

    @pytest.mark.asyncio
    async def test_http_error_handling(self, unifi_client):
        """Test HTTP error handling"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.request.side_effect = Exception("Connection error")

            with pytest.raises(HTTPException) as exc_info:
                await unifi_client.list_hosts()

            assert exc_info.value.status_code == 500
            assert "Unexpected error" in exc_info.value.detail
