"""
This module is responsible for connection handling, and provide a high-level interface for the client to send requests
and receive responses from the server.
"""

import socket
import ssl
from abc import ABC, abstractmethod


class ConfigServer(ABC):
    # TODO

    def __init__(
            self,
            server_address: str,
            port: str
    ):
        self.server_address = server_address
        self.port = port
        self.socket = None
        self.ssl_context = None
    pass
