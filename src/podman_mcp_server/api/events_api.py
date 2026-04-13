"""MCP actions related to Podman events."""

import json
import time
import requests_unixsocket

from podman_mcp_server.utils.mcp import mcpWrapper


class EventsAPI:
    @staticmethod
    @mcpWrapper.tool()
    def podman_get_events(since: str = "1m"):
        """
        Get Podman events.

        Args:
            since (str): Time range for events, e.g. "10s", "5m", "1h".
        """

        now = int(time.time())

        uri = "http+unix://%2Frun%2Fuser%2F1000%2Fpodman%2Fpodman.sock"
        endpoint = f"/v6.0.0/libpod/events?since={since}&until={now}"

        session = requests_unixsocket.Session()
        response = session.get(f"{uri}{endpoint}")
        response.raise_for_status()

        # events are newline-separated JSON, so parse each line
        events = [json.loads(line) for line in response.text.splitlines() if line.strip()]

        return events
        