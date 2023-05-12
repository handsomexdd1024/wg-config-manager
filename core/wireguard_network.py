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


class WireguardNode(ABC):
    """
    This class represents a WireGuard node.
    """

    @classmethod
    class NodeType(Enum):
        PEER = 0
        ROUTER = 1
        ROUTED = 2

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            address_list: list[IPv4Address | IPv4Network | IPv6Address | IPv6Network | None],
            node_type: NodeType = NodeType.PEER,
            private_key: bytes = None,
            public_key: bytes = None,
    ):
        """
        Initialize a WireGuard node.
        :param identifier: UUID of the node.
        :param name: Name of the node.
        :param address_list: List of addresses of the node.
        :param node_type: Type of the node. Can be one of NodeType.PEER, NodeType.ROUTER, NodeType.ROUTED.
        """
        self.name = name
        self.uuid = identifier
        self.node_type = node_type
        self.address_list = address_list
        self.private_key = private_key
        self.public_key = public_key

    def __str__(self):
        """
        Return a string representation of the node.
        :return: String representation of the node.
        """
        return f"Node {self.name} with UUID {self.uuid} and addresses {self.address_list}."


class WireguardConnection(ABC):
    """
    This class represents connections between WireGuard nodes.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            peers: (uuid.UUID, uuid.UUID),
            preshared_key: bytes | None
    ):
        self.identifier = identifier
        self.peers = peers
        self.preshared_key = preshared_key


class WireguardNetwork(ABC):
    """
    This class represents a WireGuard network.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            node_list: list[WireguardNode] = None,
            connection_list: list[WireguardConnection] = None
    ):
        """
        Initialize a WireGuard network.
        :param identifier: UUID of the network.
        :param name: Name of the network.
        :param node_list: List of the network nodes.
        :param connection_list: List of connections between network nodes.
        """
        self.name = name
        self.uuid = identifier
        self.node_list = node_list if node_list is not None else []
        self.connection_list = connection_list if connection_list is not None else []

    def __str__(self):
        """
        Return a string representation of the network.
        :return: String representation of the network.
        """
        return f"Network {self.name} with nodes {self.node_list} and edges {self.connection_list}."

    def refresh_edges(self):
        # TODO
        pass
