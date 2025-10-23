#!/usr/bin/env python3
"""
Unifi MCP Server - FastAPI application and entry point
"""
import logging
from fastapi import FastAPI

from .client import UnifiClient
from .tools import register_tools
from .resources import register_resources

try:
    from mcp import MCPServer
except Exception:  # pragma: no cover - fallback for missing MCPServer
    class MCPServer:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:
            pass

        def tool(self, *args, **kwargs):  # pragma: no cover - simple decorator
            def decorator(func):
                return func

            return decorator

        def resource(self, *args, **kwargs):  # pragma: no cover - simple decorator
            def decorator(func):
                return func

            return decorator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("unifi-mcp-server")

# Initialize FastAPI app
app = FastAPI(title="Unifi MCP Server")

# Initialize MCP Server
mcp_server = MCPServer(
    name="unifi",
    description="MCP Server for Unifi Site Manager API integration",
    app=app,
)

# Global client instance
unifi_client = None


@app.on_event("startup")
async def startup_event():
    """Initialize the Unifi client on startup"""
    global unifi_client
    try:
        unifi_client = UnifiClient()
        logger.info("Unifi client initialized successfully")

        # Register MCP tools and resources
        register_tools(mcp_server, unifi_client)
        register_resources(mcp_server, unifi_client)
        logger.info("MCP tools and resources registered successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Unifi client: {e}")
        # Stop application startup if the client is not configured
        raise RuntimeError("Unifi client initialization failed") from e


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "unifi_client_initialized": unifi_client is not None,
    }


def main():
    """Main entry point for the server"""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
