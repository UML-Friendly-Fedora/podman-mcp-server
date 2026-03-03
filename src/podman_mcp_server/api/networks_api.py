from podman_mcp_server.utils.mcp import mcpWrapper
from podman_mcp_server.utils.request import podman_get

class NetworksAPI:
	@mcpWrapper.tool()
	@staticmethod
	def podman_list_networks():
		"""List Podman Networks."""
		return podman_get("/libpod/netowrks/json")
	
	@mcpWrapper.tool()
	@staticmethod
	def podman_inspect_network(name: str):
		"""Inspect a Podman network by name"""
		return podman_get(f"/libpod/networks/{name}/json")