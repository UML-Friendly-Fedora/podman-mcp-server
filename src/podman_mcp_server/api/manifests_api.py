"""MCP actions related to Podman manifests."""

from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get


class ManifestsAPI:
    @mcpWrapper.tool(description="List local Podman manifest lists.")
    @staticmethod
    def podman_list_manifests():
        """List local Podman manifest lists."""
        # Podman does not expose a GET endpoint to list manifests directly.
        # Use image names as candidates, then keep only the names that succeed
        # when inspected through /libpod/manifests/{name}/json.
        images = podman_get("/libpod/images/json")
        if not isinstance(images, list):
            return images

        manifests = []
        seen = set()

        for img in images:
            names = img.get("Names") or []
            for name in names:
                if name in seen:
                    continue

                try:
                    manifest = podman_get(f"/libpod/manifests/{name}/json")
                    manifests.append(
                        {
                            "name": name,
                            "manifest": manifest,
                        }
                    )
                    seen.add(name)
                    break
                except Exception:
                    continue

        return manifests

    @mcpWrapper.tool(description="Inspect a Podman manifest by name.")
    @staticmethod
    def podman_inspect_manifest(name: str):
        """Inspect a Podman manifest by name."""
        return podman_get(f"/libpod/manifests/{name}/json")
