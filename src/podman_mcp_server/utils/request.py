import requests_unixsocket
import platform
import os

api_version = "v6.0.0"

session = requests_unixsocket.Session()

# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.

# Gathering the URI link for appropriate OS


def uri():
    system = platform.system()
    if system == "Darwin":
        uri = f"http+unix://%2FUsers%2F{os.environ.get('USER')}%2F.local%2Fshare%2Fcontainers%2Fpodman%2Fmachine%2Fpodman.sock"
    elif system == "Linux":
        uri = f"http+unix://{os.getenv('XDG_RUNTIME_DIR')}%2Fpodman%2Fpodman.sock"
    elif system == "Windows":
        uri = f"http+unix://{os.getenv('XDG_RUNTIME_DIR')}%2Fpodman%2Fpodman.sock"
    return uri


# TODO: Implement a unified _handle_response() helper to manage 204 No Content
# responses across podman_get(), podman_post(), and podman_delete().
# Currently only podman_get() handles 204. See issue with response.json() on empty bodies.


def podman_get(endpoint: str) -> str:
    response = session.get(f"{uri()}/{api_version}{endpoint}")
    response.raise_for_status()

    if response.status_code == 204:
        return "Status code 204: No Content. The request was successful but there is no content to return."
    if response.status_code == 404:
        return "Status code 404: Not Found. The requested resource could not be found."

    return response.json()


def podman_post(endpoint: str, data: dict) -> str:
    response = session.post(f"{uri()}/{api_version}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()
