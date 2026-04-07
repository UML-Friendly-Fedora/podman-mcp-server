"""MCP actions related to Podman pods."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class PodsAPI:
    @mcpWrapper.tool(description="Generate Systemd Units based on a pod or container.")
    @staticmethod
    def podman_generate_systemd_units(name: str):
        """Generate Systemd Unites based on a pod or container."""
        return podman_get(f"/libpod/generate/{name}/systemd")

    @mcpWrapper.tool(description="Inspect Podman pods by name.")
    @staticmethod
    def podman_inspect_pod(name: str):
        """Inspect a Podman pod by name."""
        return podman_get(f"/libpod/pods/{name}/json")

    @mcpWrapper.tool(description="List Podman pods.")
    @staticmethod
    def podman_list_pods():
        """List Podman pods."""
        return podman_get("/libpod/pods/json")

    @mcpWrapper.tool(description="List processes running inside a pod.")
    @staticmethod
    def list_pod_processes(name: str):
        """List processes running inside a pod."""
        return podman_get(f"/libpod/pods/{name}/top")

    @mcpWrapper.tool(description="Check if a pod exists by name.")
    @staticmethod
    def podman_check_pod_exists(name: str):
        """Check if a pod exists by name or ID."""
        return podman_get(f"/libpod/pods/{name}/exists")

    @mcpWrapper.tool(description="Display statistics for one or more pods.")
    @staticmethod
    def podman_check_pod_statistics():
        """Display a live stream of resource usage statistics for the containers in one or more pods."""
        return podman_get("/libpod/pods/stats")
