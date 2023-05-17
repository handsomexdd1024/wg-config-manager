# Copyright (c) 2023 Billy Yang.
# This software is licensed under the GNU AGPLv3 license.
"""
This module contains class for basic nodes and network graphs of a WireGuard network.
"""

__all__ = ["WireguardNode", "WireguardObject", "WireguardNetwork", "WireguardConnection"]

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


class WireguardObject(ABC):
    """
    This class represents an abstract Wireguard object (node, connection, network, etc.) with a unique uuid.
    """

    def __init__(self, identifier: uuid.UUID):
        """
        Initialize a WireguardObject.
        :param identifier: UUID of the object.
        """
        self.uuid = identifier

    def __eq__(self, other):
        if isinstance(other, WireguardObject):
            return self.uuid == other.uuid
        else:
            return False

    @abstractmethod
    def to_json(self) -> str:
        """
        Convert a WireguardObject object to a JSON string.
        :return: JSON string
        """
        pass


class WireguardNode(WireguardObject):
    """
    This class represents a WireGuard node.
    """

    @classmethod
    class NodeType(Enum):
        PEER = 0
        ROUTER = 1
        ROUTED = 2

    @classmethod
    class EndpointType(Enum):
        IPV4 = 0
        IPV6 = 1
        DOMAIN = 2

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            address_list: list[IPv4Address | IPv4Network | IPv6Address | IPv6Network | None],
            node_type: NodeType = NodeType.PEER,
            private_key: str = None,
            public_key: str = None,
            endpoint: (str, int) = None,
    ):
        """
        Initialize a WireGuard node.
        :param identifier: UUID of the node.
        :param name: Name of the node.
        :param address_list: List of addresses of the node.
        :param node_type: Type of the node. Can be one of NodeType.PEER, NodeType.ROUTER, NodeType.ROUTED.
        """
        super().__init__(identifier)
        self.name = name
        self.node_type = node_type
        self.address_list = address_list
        self.private_key = private_key
        self.public_key = public_key
        self.endpoint = endpoint

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
            "public_key": self.public_key,
            "endpoint": self.endpoint
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
            public_key=node["public_key"],
            endpoint=node["endpoint"]
        )


class WireguardConnection(WireguardObject):
    """
    This class represents connections between WireGuard nodes.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            peers: (uuid.UUID, uuid.UUID),
            preshared_key: str | None
    ):
        super().__init__(identifier)
        self.peers = peers
        self.preshared_key = preshared_key

    def to_json(self) -> str:
        """
        Convert a WireguardConnection object to a JSON string.
        :return: JSON string
        """
        return dumps({
            "uuid": str(self.uuid),
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


class WireguardNetwork(WireguardObject):
    """
    This class represents a WireGuard network.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            node_uuid_list: list[uuid.UUID] = None,
            connection_uuid_list: list[uuid.UUID] = None
    ):
        """
        Initialize a WireGuard network.
        :param identifier: UUID of the network.
        :param name: Name of the network.
        :param node_uuid_list: List of UUIDs of the nodes in the network.
        :param connection_uuid_list: List of UUIDs of the connections in the network.
        """
        super().__init__(identifier)
        self.name = name
        self.node_uuid_list = node_uuid_list
        self.connection_uuid_list = connection_uuid_list

    def to_json(self) -> str:
        """
        Convert a WireguardNetwork object to a JSON string.
        :return: JSON string
        """
        pass  # todo: implement this method

    @classmethod
    def from_json(cls, json_network: str):
        """
        Convert a JSON string to a WireguardNetwork object.
        :param json_network: JSON string
        :return: WireguardNetwork object
        """
        pass  # todo: implement this method

    def refresh_edges(self):
        """
        Reconstruct edges according to ip addresses and given routes.
        """
        pass  # todo: implement this method

    def gen_config(self, node_uuid: uuid.UUID):
        """
        Generate Wireguard config file for the given node.
        :param node_uuid:
        :return:
        """
        pass  # todo: decide if this method should be here or in standalone config generator
