"""MCP actions related to images."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class ImagesAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_images():
        """List Podman images."""
        return podman_get("/libpod/images/json")
