"""MCP actions related to Podman manifests."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class ManifestsAPI:
    @mcpWrapper.tool()
    @staticmethod
    def podman_list_manifests():
        """
        List local manifest lists.

        Podman does not expose a GET list endpoint for manifests.
        Get candidates from /libpod/images/json and check if they are manifests by trying to inspect them as manifests.
        """
        images = podman_get("/libpod/images/json")
        if not isinstance(images, list):
            return images

        manifests = []

        for img in images:
            names = img.get("Names") or []
            for n in names:
                base = n.split("/")[-1].split("@")[0].split(":")[0]
                try:
                    podman_get(f"/libpod/manifests/{base}/json")
                    manifests.append(img)
                    break
                except Exception:
                    continue

        return manifests

    @mcpWrapper.tool()
    @staticmethod
    def podman_inspect_manifest(name: str):
        """Inspect a manifest by name."""
        return podman_get(f"/libpod/manifests/{name}/json")