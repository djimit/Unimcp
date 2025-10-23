"""
Unit tests for Pydantic models
"""
import pytest
from pydantic import ValidationError

from unifi_mcp.models import (
    ListHostsInput,
    ListHostsOutput,
    GetHostByIdInput,
    ListSitesInput,
    ListDevicesInput,
    GetIspMetricsInput,
    QueryIspMetricsInput,
    ListSdwanConfigsInput,
    GetSdwanConfigByIdInput,
    GetSdwanConfigStatusInput,
    GetSitesInput,
    GetDevicesInput,
    GetClientsInput,
)


@pytest.mark.unit
class TestHostModels:
    """Test host management models"""

    def test_list_hosts_input_valid(self):
        """Test ListHostsInput with valid data"""
        model = ListHostsInput(page_size=50, next_token="token123")
        assert model.page_size == 50
        assert model.next_token == "token123"

    def test_list_hosts_input_optional(self):
        """Test ListHostsInput with optional fields"""
        model = ListHostsInput()
        assert model.page_size is None
        assert model.next_token is None

    def test_list_hosts_output_valid(self, sample_host_data):
        """Test ListHostsOutput with valid data"""
        model = ListHostsOutput(data=sample_host_data)
        assert model.data == sample_host_data

    def test_get_host_by_id_input_valid(self):
        """Test GetHostByIdInput with valid data"""
        model = GetHostByIdInput(host_id="host_123")
        assert model.host_id == "host_123"

    def test_get_host_by_id_input_missing_required(self):
        """Test GetHostByIdInput fails without required field"""
        with pytest.raises(ValidationError):
            GetHostByIdInput()


@pytest.mark.unit
class TestSiteModels:
    """Test site management models"""

    def test_list_sites_input_valid(self):
        """Test ListSitesInput with valid data"""
        model = ListSitesInput(page_size=25, next_token="token456")
        assert model.page_size == 25
        assert model.next_token == "token456"

    def test_list_sites_input_optional(self):
        """Test ListSitesInput with optional fields"""
        model = ListSitesInput()
        assert model.page_size is None
        assert model.next_token is None


@pytest.mark.unit
class TestDeviceModels:
    """Test device management models"""

    def test_list_devices_input_valid(self):
        """Test ListDevicesInput with valid data"""
        model = ListDevicesInput(
            host_ids=["host1", "host2"],
            time="2025-01-01T00:00:00Z",
            page_size=30,
            next_token="token789",
        )
        assert model.host_ids == ["host1", "host2"]
        assert model.time == "2025-01-01T00:00:00Z"
        assert model.page_size == 30
        assert model.next_token == "token789"

    def test_list_devices_input_optional(self):
        """Test ListDevicesInput with optional fields"""
        model = ListDevicesInput()
        assert model.host_ids is None
        assert model.time is None
        assert model.page_size is None
        assert model.next_token is None


@pytest.mark.unit
class TestISPMetricsModels:
    """Test ISP metrics models"""

    def test_get_isp_metrics_input_valid(self):
        """Test GetIspMetricsInput with valid data"""
        model = GetIspMetricsInput(
            metric_type="5m",
            begin_timestamp="2025-01-01T00:00:00Z",
            end_timestamp="2025-01-02T00:00:00Z",
            duration="24h",
        )
        assert model.metric_type == "5m"
        assert model.begin_timestamp == "2025-01-01T00:00:00Z"
        assert model.end_timestamp == "2025-01-02T00:00:00Z"
        assert model.duration == "24h"

    def test_get_isp_metrics_input_required_only(self):
        """Test GetIspMetricsInput with only required field"""
        model = GetIspMetricsInput(metric_type="1h")
        assert model.metric_type == "1h"
        assert model.begin_timestamp is None

    def test_get_isp_metrics_input_missing_required(self):
        """Test GetIspMetricsInput fails without required field"""
        with pytest.raises(ValidationError):
            GetIspMetricsInput()

    def test_query_isp_metrics_input_valid(self):
        """Test QueryIspMetricsInput with valid data"""
        query_data = {"sites": ["site1"], "metrics": ["download"]}
        model = QueryIspMetricsInput(query_data=query_data)
        assert model.query_data == query_data

    def test_query_isp_metrics_input_missing_required(self):
        """Test QueryIspMetricsInput fails without required field"""
        with pytest.raises(ValidationError):
            QueryIspMetricsInput()


@pytest.mark.unit
class TestSDWANModels:
    """Test SD-WAN management models"""

    def test_list_sdwan_configs_input_valid(self):
        """Test ListSdwanConfigsInput with valid data"""
        model = ListSdwanConfigsInput(page_size=20, next_token="token_sdwan")
        assert model.page_size == 20
        assert model.next_token == "token_sdwan"

    def test_get_sdwan_config_by_id_input_valid(self):
        """Test GetSdwanConfigByIdInput with valid data"""
        model = GetSdwanConfigByIdInput(config_id="config_123")
        assert model.config_id == "config_123"

    def test_get_sdwan_config_by_id_input_missing_required(self):
        """Test GetSdwanConfigByIdInput fails without required field"""
        with pytest.raises(ValidationError):
            GetSdwanConfigByIdInput()

    def test_get_sdwan_config_status_input_valid(self):
        """Test GetSdwanConfigStatusInput with valid data"""
        model = GetSdwanConfigStatusInput(config_id="config_456")
        assert model.config_id == "config_456"


@pytest.mark.unit
class TestLegacyModels:
    """Test legacy backward compatibility models"""

    def test_get_sites_input_valid(self):
        """Test GetSitesInput (no fields)"""
        model = GetSitesInput()
        assert model is not None

    def test_get_devices_input_valid(self):
        """Test GetDevicesInput with valid data"""
        model = GetDevicesInput(site_id="site_123")
        assert model.site_id == "site_123"

    def test_get_devices_input_missing_required(self):
        """Test GetDevicesInput fails without required field"""
        with pytest.raises(ValidationError):
            GetDevicesInput()

    def test_get_clients_input_valid(self):
        """Test GetClientsInput with valid data"""
        model = GetClientsInput(site_id="site_456")
        assert model.site_id == "site_456"

    def test_get_clients_input_missing_required(self):
        """Test GetClientsInput fails without required field"""
        with pytest.raises(ValidationError):
            GetClientsInput()
