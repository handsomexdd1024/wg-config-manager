# Copyright (c) 2023 Billy Yang.
# This software is licensed under the GNU AGPLv3 license.
"""
This module contains class for basic nodes and network graphs of a WireGuard network.
"""

from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network
)
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from wireguard_tools.wireguard_key import *


class NodeType(Enum):
    PEER = 0
    ROUTER = 1
    ROUTED = 2


class WireGuardNode(ABC):
    """
    This class represents a WireGuard node.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            node_type: NodeType,
            address_list: list[IPv4Address | IPv4Network | IPv6Address | IPv6Network]
    ):
        """
        Initialize a WireGuard node.
        :param name: Name of the node.
        :param node_type: Type of the node.
        :param address_list: List of addresses of the node.
        """
        self.name = name
        self.uuid = identifier
        self.node_type = node_type
        self.address_list = address_list
        self.private_key = WireguardKey.generate()
        self.public_key = self.private_key.public_key()

    def __str__(self):
        """
        Return a string representation of the node.
        :return: String representation of the node.
        """
        return f"Node {self.name} ({self.node_type}) with addresses {self.address_list}."


class WireGuardNetwork(ABC):
    """
    This class represents a WireGuard network.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            node_list: list[WireGuardNode] = None,
            edge_list: list[tuple[WireGuardNode, WireGuardNode]] = None
    ):
        self.name = name
        self.uuid = identifier
        self.node_list = node_list if node_list is not None else []
        self.edge_list = edge_list if edge_list is not None else []

    def __str__(self):
        """
        Return a string representation of the network.
        :return: String representation of the network.
        """
        return f"Network {self.name} with nodes {self.node_list} and edges {self.edge_list}."

    def refresh_edges(self):
        # TODO
        pass
