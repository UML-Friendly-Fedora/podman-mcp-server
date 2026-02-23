from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class VolumesAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_volumes():
        """List Podman volumes."""
        return podman_get("/libpod/volumes/json")

    @mcpWrapper.tool()
    @staticmethod
    def podman_inspect_volume(name: str):
        """Inspect a Podman volume by name."""
        return podman_get(f"/libpod/volumes/{name}/json")
