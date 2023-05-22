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
from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
import json
from wireguard_tools.wireguard_key import (
    WireguardKey,
    convert_wireguard_key
)


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


class WireguardNode(WireguardObject):
    """
    This class represents a WireGuard node.
    """

    class NodeType(Enum):
        PEER = 0
        ROUTER = 1
        ROUTED = 2

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
            public_key: WireguardKey = None,
            private_key: WireguardKey = None,
            endpoint: (str, int) = None,
    ):
        """
        Initialize a WireGuard node.
        """
        super().__init__(identifier)
        self.owner = owner
        self.name = name
        self.admin_approval = admin_approval
        self.node_type = node_type
        self.address_list = address_list
        if private_key is not None:
            self.private_key = private_key
            if public_key is not None:
                if private_key.public_key() != public_key:
                    raise ValueError("Cannot specify both private key and public key.")
                else:
                    self.public_key = public_key
            else:
                self.public_key = private_key.public_key()
        elif public_key is not None:
            self.public_key = public_key
        else:
            raise ValueError("Must specify either private key or public key.")
        self.endpoint = endpoint

    @staticmethod
    def default_encoder(o):
        """
        Msgpack encoder for WireguardNode.
        :param o: WireguardNode object.
        :return: Dict of WireguardNode.
        """
        if isinstance(o, WireguardNode):
            return {
                "__WireguardNode__": True,
                "uuid": o.uuid.bytes,
                "owner": o.owner.bytes,
                "name": o.name,
                "admin_approval": o.admin_approval,
                "node_type": o.node_type.value,
                "address_list": [str(i) for i in o.address_list],
                "public_key": o.public_key.keydata if o.public_key is not None else None,
                "private_key": o.private_key.keydata if o.private_key is not None else None,
                "endpoint": o.endpoint
            }

    @staticmethod
    def default_decoder(o):
        """
        Msgpack decoder for WireguardNode.
        :param o: Dict of WireguardNode.
        :return: WireguardNode object.
        """
        if "__WireguardNode__" in o:
            return WireguardNode(
                identifier=uuid.UUID(bytes=o["uuid"]),
                owner=uuid.UUID(bytes=o["owner"]),
                name=o["name"],
                admin_approval=o["admin_approval"],
                node_type=WireguardNode.NodeType(o["node_type"]),
                address_list=[i for i in o["address_list"]],
                public_key=WireguardKey(o["public_key"]) if o["public_key"] is not None else None,
                private_key=WireguardKey(o["private_key"]) if o["private_key"] is not None else None,
                endpoint=o["endpoint"]
            )
        else:
            raise ValueError("Not a WireguardNode object.")


class WireguardConnection(WireguardObject):
    """
    This class represents connections between WireGuard nodes.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            peers: (uuid.UUID, uuid.UUID),
            preshared_key: WireguardKey | None
    ):
        super().__init__(identifier)
        self.peers = peers
        self.preshared_key = preshared_key

    @staticmethod
    def default_encoder(o):
        """
        Msgpack encoder for WireguardConnection.
        :param o: WireguardConnection object.
        :return: Dict of WireguardConnection.
        """
        if isinstance(o, WireguardConnection):
            return {
                "__WireguardConnection__": True,
                "uuid": o.uuid.bytes,
                "peers": [i.bytes for i in o.peers],
                "preshared_key": o.preshared_key.keydata if o.preshared_key is not None else None
            }
        else:
            raise ValueError("Not a WireguardConnection object.")

    @staticmethod
    def default_decoder(o):
        """
        Msgpack decoder for WireguardConnection.
        :param o: Dict of WireguardConnection.
        :return: WireguardConnection object.
        """
        if "__WireguardConnection__" in o:
            return WireguardConnection(
                identifier=uuid.UUID(bytes=o["uuid"]),
                peers=[uuid.UUID(bytes=i) for i in o["peers"]],
                preshared_key=WireguardKey(o["preshared_key"]) if o["preshared_key"] is not None else None
            )
        else:
            raise ValueError("Not a WireguardConnection object.")


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

    @staticmethod
    def default_encoder(o):
        """
        Msgpack encoder for WireguardNetwork.
        :param o: WireguardNetwork object.
        :return: Dict of WireguardNetwork.
        """
        if isinstance(o, WireguardNetwork):
            return {
                "__WireguardNetwork__": True,
                "uuid": o.uuid.bytes,
                "name": o.name,
                "node_uuid_list": [i.bytes for i in o.node_uuid_list],
                "connection_uuid_list": [i.bytes for i in o.connection_uuid_list]
            }
        else:
            raise ValueError("Not a WireguardNetwork object.")

    @staticmethod
    def default_decoder(o):
        """
        Msgpack decoder for WireguardNetwork.
        :param o: Dict of WireguardNetwork.
        :return: WireguardNetwork object.
        """
        if "__WireguardNetwork__" in o:
            return WireguardNetwork(
                identifier=uuid.UUID(bytes=o["uuid"]),
                name=o["name"],
                node_uuid_list=[uuid.UUID(bytes=i) for i in o["node_uuid_list"]],
                connection_uuid_list=[uuid.UUID(bytes=i) for i in o["connection_uuid_list"]]
            )
        else:
            raise ValueError("Not a WireguardNetwork object.")
