import requests_unixsocket

# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.

uri = "http+unix://%2Frun%2Fuser%2F1000%2Fpodman%2Fpodman.sock"
api_version = "v6.0.0"

session = requests_unixsocket.Session()


# TODO: Implement a unified _handle_response() helper to manage 204 No Content
# responses across podman_get(), podman_post(), and podman_delete().
# Currently only podman_get() handles 204. See issue with response.json() on empty bodies.


def podman_get(endpoint: str) -> str:
    response = session.get(f"{uri}/{api_version}{endpoint}")
    response.raise_for_status()

    if response.status_code == 204:
        return "Status code 204: No Content. The request was successful but there is no content to return."
    if response.status_code == 404:
        return "Status code 404: Not Found. The requested resource could not be found."

    return response.json()


def podman_post(endpoint: str, data: dict) -> str:
    response = session.post(f"{uri}/{api_version}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()
