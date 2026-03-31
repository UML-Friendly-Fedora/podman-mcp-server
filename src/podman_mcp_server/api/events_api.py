"""MCP actions related to Podman events."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class EventsAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_get_events():
        """Get Podman events."""
        return podman_get("/libpod/events?since=1m")