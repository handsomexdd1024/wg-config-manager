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
            owner: uuid.UUID,
            name: str,
            address_list: list[IPv4Address | IPv4Network | IPv6Address | IPv6Network | None],
            admin_approval: bool = True,
            node_type: NodeType = NodeType.PEER,
            public_key: str = None,
            private_key: str = None,
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
        self.owner = owner
        self.name = name
        self.admin_approval = admin_approval
        self.node_type = node_type
        self.address_list = address_list
        self.private_key = private_key
        self.public_key = public_key
        self.endpoint = endpoint


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
