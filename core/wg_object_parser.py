# Copyright (c) 2023 Billy Yang
# This software is licensed under the GNU AGPLv3 license.

"""
Parser of Wireguard objects.
"""

from json import loads, dumps
import core
from core import (
    WireguardNode,
    WireguardConnection,
    WireguardNetwork
)


def node2json(
        node: WireguardNode
) -> str:
    """
    Convert a WireguardNode object to a JSON string.
    :param node: WireguardNode object
    :return: JSON string
    """
    return dumps({
        "name": node.name,
        "uuid": str(node.uuid),
        "node_type": node.node_type,
        "address_list": node.address_list,
        "private_key": node.private_key,
        "public_key": node.public_key
    },
        ensure_ascii=False
    )


def json2node(
        json_node: str
) -> WireguardNode:
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


def edge2json(
        edge: WireguardConnection
) -> str:
    """
    Convert a WireguardConnection object to a JSON string.
    :param edge: WireguardConnection object
    :return: JSON string
    """
    return dumps({
        "uuid": str(edge.identifier),
        "peers": (str(edge.peers[0]), str(edge.peers[1])),
        "preshared_key": edge.preshared_key
    },
        ensure_ascii=False
    )


def json2edge(
        json_edge: str
) -> WireguardConnection:
    """
    Convert a JSON string to a WireguardConnection object.
    :param json_edge: JSON string
    :return: WireguardConnection object
    """
    edge = loads(json_edge)
    return WireguardConnection(
        identifier=edge["uuid"],
        peers=(edge["peers"][0], edge["peers"][1]),
        preshared_key=edge["preshared_key"]
    )


def network2json(
        network: WireguardNetwork
) -> str:
    """
    Convert a WireguardNetwork object to a JSON string.
    :param network: WireguardNetwork object
    :return: JSON string
    """
    return dumps({
        "name": network.name,
        "uuid": str(network.uuid),
        "node_list": [node2json(node) for node in network.node_list],
        "connection_list": [edge2json(edge) for edge in network.connection_list]
    },
        ensure_ascii=False
    )


def json2network(
        json_network: str
) -> WireguardNetwork:
    """
    Convert a JSON string to a WireguardNetwork object.
    :param json_network: JSON string
    :return: WireguardNetwork object
    """
    network = loads(json_network)
    return WireguardNetwork(
        name=network["name"],
        identifier=network["uuid"],
        node_list=[json2node(node) for node in network["node_list"]],
        connection_list=[json2edge(edge) for edge in network["connection_list"]]
    )
