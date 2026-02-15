"""MCP actions related to containers."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class ContainersAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_containers():
        """List Podman containers."""
        return podman_get("/libpod/containers/json")

    @mcpWrapper.tool()
    @staticmethod
    def list_processes(container_id: str):
        """List processes running in a container."""
        return podman_get(f"/libpod/containers/{container_id}/top")
