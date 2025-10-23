"""
Pytest configuration and fixtures
"""
import os
import pytest
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_env(monkeypatch):
    """Set up mock environment variables"""
    monkeypatch.setenv("UNIFI_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("UNIFI_API_URL", "https://api.ui.com")
    yield
    monkeypatch.delenv("UNIFI_API_KEY", raising=False)
    monkeypatch.delenv("UNIFI_API_URL", raising=False)


@pytest.fixture
def sample_host_data():
    """Sample host data for testing"""
    return {
        "data": [
            {
                "id": "host_123",
                "name": "Test Host",
                "status": "online",
                "ip": "192.168.1.1",
                "type": "UDM-PRO",
            }
        ],
        "nextToken": "next_page_token",
    }


@pytest.fixture
def sample_site_data():
    """Sample site data for testing"""
    return {
        "data": [
            {
                "id": "site_456",
                "name": "Test Site",
                "description": "Test site description",
                "hostId": "host_123",
            }
        ],
        "nextToken": None,
    }


@pytest.fixture
def sample_device_data():
    """Sample device data for testing"""
    return {
        "data": [
            {
                "id": "device_789",
                "name": "Test Device",
                "type": "UAP",
                "model": "U6-LR",
                "status": "connected",
                "mac": "00:11:22:33:44:55",
            }
        ],
        "nextToken": None,
    }


@pytest.fixture
def sample_isp_metrics_data():
    """Sample ISP metrics data for testing"""
    return {
        "data": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "download": 100.5,
                "upload": 50.2,
                "latency": 10,
            }
        ]
    }


@pytest.fixture
def sample_sdwan_config_data():
    """Sample SD-WAN config data for testing"""
    return {
        "data": [
            {
                "id": "config_123",
                "name": "Test SD-WAN Config",
                "status": "active",
                "created": "2025-01-01T00:00:00Z",
            }
        ],
        "nextToken": None,
    }


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx response"""

    class MockResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")

        def json(self):
            return self._data

    return MockResponse


@pytest.fixture
async def mock_httpx_client(mock_httpx_response):
    """Create a mock httpx client"""
    mock_client = AsyncMock()
    mock_instance = AsyncMock()

    # Configure the context manager
    mock_client.return_value.__aenter__.return_value = mock_instance

    return mock_client, mock_instance


@pytest.fixture
def unifi_client(mock_env):
    """Create a UnifiClient instance with mocked environment"""
    from unifi_mcp.client import UnifiClient

    return UnifiClient()
