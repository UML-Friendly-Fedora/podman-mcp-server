"""MCP actions related to Podman engine."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class SystemAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_version():
        """Get the version of Podman."""
        return podman_get("/libpod/version")

    @mcpWrapper.tool()
    @staticmethod
    def podman_info():
        """Get information about Podman."""
        return podman_get("/libpod/info")
