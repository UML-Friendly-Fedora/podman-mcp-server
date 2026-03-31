"""MCP actions related to artifacts."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class ArtifactsAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_artifacts():
        """List Podman artifacts."""
        return podman_get("/libpod/artifacts/json")
    
    @mcpWrapper.tool()
    @staticmethod
    def get_artifact(artifact_id: str):
        """Get details of a specific artifact."""
        return podman_get(f"/libpod/artifacts/{artifact_id}/json")
