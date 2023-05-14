"""
This module is responsible for connection handling, and provide a high-level interface for the client to send requests
and receive responses from the server.
"""

import socket
import ssl
from abc import ABC, abstractmethod

import core.wireguard_object_pb2 as wg_obj


class ConfigServer(ABC):
    # TODO
    pass
