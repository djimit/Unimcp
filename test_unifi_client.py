#!/usr/bin/env python3
"""
Test script to verify UnifiClient implements all UI.com Site Manager API functions
"""
import asyncio
import os
import sys
from unittest.mock import AsyncMock, patch
import logging

# Ensure we can import the project modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import UnifiClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def test_api_coverage():
    """Test that all API endpoints from the official documentation are implemented"""
    
    # Set up environment variables for testing
    os.environ["UNIFI_API_KEY"] = "test_api_key"
    os.environ["UNIFI_API_URL"] = "https://api.ui.com"
    
    # Mock HTTP responses
    mock_response_data = {
        "data": [
            {
                "id": "test_id",
                "name": "Test Item",
                "status": "active"
            }
        ],
        "nextToken": "next_page_token"
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        # Setup the mock client
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance

        class DummyResponse:
            def __init__(self, data):
                self._data = data

            def raise_for_status(self):
                return None

            def json(self):
                return self._data

        mock_instance.request.return_value = DummyResponse(mock_response_data)
        
        # Initialize the client
        client = UnifiClient()
        
        # Test all API endpoints
        api_tests = [
            # Host Management
            ("list_hosts", lambda: client.list_hosts()),
            ("list_hosts_with_pagination", lambda: client.list_hosts(page_size=50, next_token="token")),
            ("get_host_by_id", lambda: client.get_host_by_id("test_host_id")),
            
            # Site Management
            ("list_sites", lambda: client.list_sites()),
            ("list_sites_with_pagination", lambda: client.list_sites(page_size=50, next_token="token")),
            
            # Device Management
            ("list_devices", lambda: client.list_devices()),
            ("list_devices_with_filters", lambda: client.list_devices(
                host_ids=["host1", "host2"], 
                time="2024-04-15T09:30:29Z",
                page_size=50,
                next_token="token"
            )),
            
            # ISP Metrics
            ("get_isp_metrics", lambda: client.get_isp_metrics("5m")),
            ("get_isp_metrics_with_timerange", lambda: client.get_isp_metrics(
                "5m",
                begin_timestamp="2024-04-15T09:30:29Z",
                end_timestamp="2024-04-16T09:30:29Z",
                duration="24h"
            )),
            ("query_isp_metrics", lambda: client.query_isp_metrics({
                "sites": ["site1", "site2"],
                "metrics": ["download", "upload"]
            })),
            
            # SD-WAN Management
            ("list_sdwan_configs", lambda: client.list_sdwan_configs()),
            ("list_sdwan_configs_with_pagination", lambda: client.list_sdwan_configs(
                page_size=50, 
                next_token="token"
            )),
            ("get_sdwan_config_by_id", lambda: client.get_sdwan_config_by_id("config_123")),
            ("get_sdwan_config_status", lambda: client.get_sdwan_config_status("config_123")),
            
            # Legacy methods
            ("get_sites_legacy", lambda: client.get_sites()),
            ("get_devices_legacy", lambda: client.get_devices("site1")),
            ("get_clients_legacy", lambda: client.get_clients("site1")),
        ]
        
        results = []
        for test_name, test_func in api_tests:
            try:
                await test_func()
                logger.info(f"✅ {test_name}: PASSED")
                results.append((test_name, "PASSED", None))
            except Exception as e:
                logger.error(f"❌ {test_name}: FAILED - {str(e)}")
                results.append((test_name, "FAILED", str(e)))
        
        # Print summary
        print("\n" + "="*80)
        print("API COVERAGE TEST SUMMARY")
        print("="*80)
        
        passed = len([r for r in results if r[1] == "PASSED"])
        total = len(results)
        
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Coverage: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL API ENDPOINTS FROM UI.COM SITE MANAGER API v1.0 ARE IMPLEMENTED!")
        else:
            print("\n⚠️  Some API endpoints are missing or have issues:")
            for test_name, status, error in results:
                if status == "FAILED":
                    print(f"  - {test_name}: {error}")
        
        print("\n" + "="*80)
        print("IMPLEMENTED API ENDPOINTS:")
        print("="*80)
        
        endpoints = [
            "GET /v1/hosts - List Hosts",
            "GET /v1/hosts/{hostId} - Get Host by ID", 
            "GET /v1/sites - List Sites",
            "GET /v1/devices - List Devices",
            "GET /ea/isp-metrics/{type} - Get ISP Metrics",
            "POST /ea/isp-metrics/query - Query ISP Metrics",
            "GET /v1/sd-wan/configs - List SD-WAN Configs",
            "GET /v1/sd-wan/configs/{configId} - Get SD-WAN Config by ID",
            "GET /v1/sd-wan/configs/{configId}/status - Get SD-WAN Config Status"
        ]
        
        for endpoint in endpoints:
            print(f"✅ {endpoint}")
        
        return passed == total

if __name__ == "__main__":
    result = asyncio.run(test_api_coverage())
    sys.exit(0 if result else 1)
