import socket
import threading
from functools import partial
from getpass import getuser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import List
from urllib.parse import urlparse
import requests


def get_routable_ip_to(addr: str) -> str:
    """
    get_routable_ip_to opens a dummy connection to the target HTTP URL and
    returns the IP address used to connect to it.
    """
    parsed = urlparse(addr)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((parsed.hostname, parsed.port or 80))
        return s.getsockname()[0]
    finally:
        s.close()
        
        
def send_model_to_torchserve(
    management_api: str,
    local_serving_directory: str,
    archived_model_file_name: str,
    torchserve_params: dict,
    model_name: str,
    model_version: str,
    timeout: int,
    port: int,
    ):
    
    addr = ("", port)
    print(f"starting HTTP server at {addr}...")

    handler_class = partial(SimpleHTTPRequestHandler, directory=local_serving_directory)
    server: ThreadingHTTPServer = ThreadingHTTPServer(addr, handler_class)

    try:

        def serve() -> None:
            server.serve_forever()

        t = threading.Thread(target=serve)
        t.start()

        ip_address = get_routable_ip_to(management_api)
        model_url = f"http://{ip_address}:{server.server_port}/{archived_model_file_name}.mar"
        print(f"serving file at {model_url}")

        url = f"{management_api}/models"
        print(f"POST {url}")
        payload = {
            "url": model_url,
            "initial_workers": 1,
            "model_name": model_name,
            "version": model_version,
        }
        r = requests.post(url, params=payload, timeout=timeout)

        return r

    finally:
        print("shutting down...")
        server.shutdown()