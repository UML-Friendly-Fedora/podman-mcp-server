"""Podman MCP Server"""

import json
from pydantic import Field
import requests
import requests_unixsocket
from mcp.server.fastmcp import FastMCP

# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.

uri = "http+unix://%2Frun%2Fuser%2F1000%2Fpodman%2Fpodman.sock"
api_version = "v6.0.0"

mcp = FastMCP("Podman MCP Server")
session = requests_unixsocket.Session()


def podman_get(endpoint: str) -> str:
    response = session.get(f"{uri}/{api_version}{endpoint}")
    response.raise_for_status()
    return response.json()


def podman_post(endpoint: str, data: dict) -> str:
    response = session.post(f"{uri}/{api_version}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def podman_version():
    """Get the version of Podman."""
    return podman_get("/libpod/version")


@mcp.tool()
def podman_info():
    """Get information about Podman."""
    return podman_get("/libpod/info")


@mcp.tool()
def podman_list_containers():
    """List Podman containers."""
    return podman_get("/libpod/containers/json")


@mcp.tool()
def podman_list_images():
    """List Podman images."""
    return podman_get("/libpod/images/json")


@mcp.tool()
def list_processes(container_id: str):
    """List processes running in a container."""
    return podman_get(f"/libpod/containers/{container_id}/top")


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
