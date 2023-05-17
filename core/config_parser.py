"""
Configuration file parser for core module.
Generate configuration files from given wireguard network object, and vice versa.
"""

import yaml
from uuid import UUID
from core.wgobject import *


class ConfigParser:
    """
    Parse WireguardNetwork object into Wireguard configuration files.
    """

    def load_network(self, network: WireguardNetwork):
        self.network = network

    def __init__(self, network: WireguardNetwork):
        self.network = network

    def generate_config(self, node_id: UUID):
        pass  # todo
