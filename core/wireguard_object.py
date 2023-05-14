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
from json import loads, dumps
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
            private_key: str = None,
            public_key: str = None,
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

    # convert to json
    def to_json(self) -> str:
        """
        Convert a WireguardNode object to a JSON string.
        :return: JSON string
        """
        return dumps({
            "name": self.name,
            "uuid": str(self.uuid),
            "node_type": self.node_type,
            "address_list": self.address_list,
            "private_key": self.private_key,
            "public_key": self.public_key
        },
            ensure_ascii=False
        )

    @classmethod
    def from_json(cls, json_node: str):
        """
        Convert a JSON string to a WireguardNode object.
        :param json_node: JSON string
        :return: WireguardNode object
        """
        node = loads(json_node)
        return WireguardNode(
            name=node["name"],
            identifier=node["uuid"],
            node_type=node["node_type"],
            address_list=node["address_list"],
            private_key=node["private_key"],
            public_key=node["public_key"]
        )


class WireguardConnection(ABC):
    """
    This class represents connections between WireGuard nodes.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            peers: (uuid.UUID, uuid.UUID),
            preshared_key: str | None
    ):
        self.identifier = identifier
        self.peers = peers
        self.preshared_key = preshared_key

    def to_json(self) -> str:
        """
        Convert a WireguardConnection object to a JSON string.
        :return: JSON string
        """
        return dumps({
            "uuid": str(self.identifier),
            "peers": self.peers,
            "preshared_key": self.preshared_key
        },
            ensure_ascii=False
        )

    @classmethod
    def from_json(cls, json_connection: str):
        """
        Convert a JSON string to a WireguardConnection object.
        :param json_connection: JSON string
        :return: WireguardConnection object
        """
        connection = loads(json_connection)
        return WireguardConnection(
            identifier=connection["uuid"],
            peers=connection["peers"],
            preshared_key=connection["preshared_key"]
        )


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

    def to_json(self) -> str:
        """
        Convert a WireguardNetwork object to a JSON string.
        :return: JSON string
        """
        return dumps({
            "name": self.name,
            "uuid": str(self.uuid),
            "node_list": [node.to_json() for node in self.node_list],
            "connection_list": [connection.to_json() for connection in self.connection_list]
        },
            ensure_ascii=False
        )

    @classmethod
    def from_json(cls, json_network: str):
        """
        Convert a JSON string to a WireguardNetwork object.
        :param json_network: JSON string
        :return: WireguardNetwork object
        """
        network = loads(json_network)
        return WireguardNetwork(
            name=network["name"],
            identifier=network["uuid"],
            node_list=[WireguardNode.from_json(node) for node in network["node_list"]],
            connection_list=[WireguardConnection.from_json(connection) for connection in network["connection_list"]]
        )

    def refresh_edges(self):
        # TODO
        pass
