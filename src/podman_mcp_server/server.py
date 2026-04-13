"""Podman MCP Server"""

from mcp.server.fastmcp import FastMCP
from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.api import system_api, containers_api, images_api, networks_api, volumes_api, manifests_api, events_api


def main():
    """Run the MCP server."""
    mcp = FastMCP("Podman MCP Server")

    # Dummy calls to avoid "unused" errors.
    # The mcpWrapper will handle adding the tools to the MCP instance.
    system_api.SystemAPI()
    containers_api.ContainersAPI()
    images_api.ImagesAPI()
    networks_api.NetworksAPI()
    volumes_api.VolumesAPI()
    manifests_api.ManifestsAPI()
    events_api.EventsAPI()
    
    # Initialize the mcpWrapper with the MCP instance
    mcpWrapper(mcp)
    mcp.run()


if __name__ == "__main__":
    main()
