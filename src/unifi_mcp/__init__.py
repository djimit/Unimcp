"""
Unifi MCP Server - Integrates UniFi Site Manager API with Claude Desktop
"""

__version__ = "1.0.0"
__author__ = "Unifi MCP Server Contributors"
__license__ = "MIT"

from .client import UnifiClient
from .server import app

__all__ = ["UnifiClient", "app", "__version__"]
