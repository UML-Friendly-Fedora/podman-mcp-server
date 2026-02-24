import requests_unixsocket

# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.

uri = "http+unix://%2Frun%2Fuser%2F1000%2Fpodman%2Fpodman.sock"
api_version = "v6.0.0"

session = requests_unixsocket.Session()


def podman_get(endpoint: str) -> str:
    response = session.get(f"{uri}/{api_version}{endpoint}")
    response.raise_for_status()
    return response.json()


def podman_post(endpoint: str, data: dict) -> str:
    response = session.post(f"{uri}/{api_version}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()
