"""
Pydantic models for MCP tools input/output
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


# Host Management Models
class ListHostsInput(BaseModel):
    page_size: Optional[int] = Field(
        None, description="Number of items to return per page"
    )
    next_token: Optional[str] = Field(
        None, description="Token for pagination to retrieve the next set of results"
    )


class ListHostsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Host data from API response")


class GetHostByIdInput(BaseModel):
    host_id: str = Field(..., description="Unique identifier of the host")


class GetHostByIdOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Host details")


# Site Management Models
class ListSitesInput(BaseModel):
    page_size: Optional[int] = Field(
        None, description="Number of items to return per page"
    )
    next_token: Optional[str] = Field(
        None, description="Token for pagination to retrieve the next set of results"
    )


class ListSitesOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Sites data from API response")


# Device Management Models
class ListDevicesInput(BaseModel):
    host_ids: Optional[List[str]] = Field(
        None, description="List of host IDs to filter the results"
    )
    time: Optional[str] = Field(
        None, description="Last processed timestamp of devices in RFC3339 format"
    )
    page_size: Optional[int] = Field(
        None, description="Number of items to return per page"
    )
    next_token: Optional[str] = Field(
        None, description="Token for pagination to retrieve the next set of results"
    )


class ListDevicesOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Devices data from API response")


# ISP Metrics Models
class GetIspMetricsInput(BaseModel):
    metric_type: str = Field(..., description="Type of metrics (5m or 1h intervals)")
    begin_timestamp: Optional[str] = Field(
        None, description="The earliest timestamp to retrieve data from (RFC3339 format)"
    )
    end_timestamp: Optional[str] = Field(
        None, description="The latest timestamp to retrieve data up to (RFC3339 format)"
    )
    duration: Optional[str] = Field(
        None, description="Specifies the time range of metrics to retrieve"
    )


class GetIspMetricsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="ISP metrics data")


class QueryIspMetricsInput(BaseModel):
    query_data: Dict[str, Any] = Field(..., description="Query parameters for ISP metrics")


class QueryIspMetricsOutput(BaseModel):
    data: Dict[str, Any] = Field(..., description="Queried ISP metrics data")


# SD-WAN Management Models
class ListSdwanConfigsInput(BaseModel):
    page_size: Optional[int] = Field(
        None, description="Number of items to return per page"
    )
    next_token: Optional[str] = Field(
        None, description="Token for pagination to retrieve the next set of results"
    )


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
        ..., description="List of devices for the specified site"
    )


class GetClientsInput(BaseModel):
    site_id: str = Field(..., description="ID of the site to get clients for")


class GetClientsOutput(BaseModel):
    clients: List[Dict[str, Any]] = Field(
        ..., description="List of clients for the specified site"
    )
