"""MCP actions related to networks."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class NetworksAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_networks():
        """List Podman networks."""
        return podman_get("/libpod/networks/json")
    
