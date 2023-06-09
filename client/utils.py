import secrets

from object_loader import ObjectLoader
from core import *
from uuid import UUID, uuid4
from enum import Enum

import wireguard_tools as wgtools


def gen_config(
        loader: ObjectLoader,
        node_id: UUID
) -> wgtools.WireguardConfig:
    # security checks
    if node_id not in loader:
        raise ValueError("Node not found in cache.")
    node = loader[node_id]
    if not isinstance(node, wgconfig.WireguardNode):
        raise ValueError("Object is not a WireguardNode.")

    conf = wgtools.WireguardConfig.from_dict(
        {
            "private_key": node.private_key.keydata if node.private_key is not None else None,
            "listen_port": node.endpoint[1],
            "addresses": node.address_list,
            "peers": []
        }
    )

    for cid in node.connection_list:
        if cid not in loader:
            raise ValueError("Connection not found in cache.")
        connection = loader[cid]
        if not isinstance(connection, wgconfig.WireguardConnection):
            raise ValueError("Object is not a WireguardConnection.")
        if connection.peers[0] == node_id:
            peer_id = connection.peers[1]
        elif connection.peers[1] == node_id:
            peer_id = connection.peers[0]
        else:
            raise ValueError("Connection does not contain this node.")
        if peer_id not in loader:
            raise ValueError("Peer not found in cache.")

        peer = loader[peer_id]
        if not isinstance(peer, wgconfig.WireguardNode):
            raise ValueError("Object is not a WireguardNode.")

        peer_conf = wgtools.wireguard_config.WireguardPeer.from_dict({
            "public_key": peer.public_key.keydata if peer.public_key is not None else None,
            "endpoint": peer.endpoint,
            "allowed_ips": peer.address_list,
            "preshared_key": connection.preshared_key.keydata if connection.preshared_key is not None else None
        })

        conf.add_peer(peer_conf)

    return conf


class ConstructType(Enum):
    """
    This enum is used to specify the type of auto_construct.
    """
    P2P = 0
    STAR = 1


def _auto_construct_p2p(
        node_id_list: list[UUID],
        loader: ObjectLoader
) -> list[wgobject.WireguardConnection]:
    nodes = []
    for nid in node_id_list:
        node = loader[nid]
        if node.endpoint is None:
            raise ValueError("Node has no endpoint, cannot construct full-mesh network.")
        nodes.append(node)
    connections = []
    # for each two nodes, construct a connection with a preshared key
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            connection = wgobject.WireguardConnection(
                identifier=UUID(bytes=uuid4().bytes),
                preshared_key=wgobject.WireguardKey(
                    keydata=secrets.token_bytes(32)
                ),
                peers=[nodes[i].identifier, nodes[j].identifier]
            )
            connections.append(connection)
    return connections


def _auto_construct_star(
        node_id_list: list[UUID],
        loader: ObjectLoader
) -> list[wgobject.WireguardConnection]:
    clients = []
    router = None
    connections = []
    for nid in node_id_list:
        node = loader[nid]
        if node.endpoint is not None:
            if router is not None:
                raise ValueError("More than one node has an endpoint, cannot construct star network.")
            router = node
        else:
            clients.append(node)
    if router is None:
        raise ValueError("No node has an endpoint, cannot construct star network.")
    for client in clients:
        connection = wgobject.WireguardConnection(
            identifier=UUID(bytes=uuid4().bytes),
            preshared_key=wgobject.WireguardKey(
                keydata=secrets.token_bytes(32)
            ),
            peers=[router.identifier, client.identifier]
        )
        connections.append(connection)
    return connections


def auto_construct(
        node_id_list: [UUID],
        loader: ObjectLoader,
        construct_type: ConstructType
) -> list[wgobject.WireguardConnection] :
    # security checks
    for nid in node_id_list:
        if nid not in loader:
            raise ValueError("Node not found in cache.")
        node = loader[nid]
        if not isinstance(node, wgconfig.WireguardNode):
            raise ValueError("Object is not a WireguardNode.")

    # construct
    if construct_type == ConstructType.P2P:
        return _auto_construct_p2p(node_id_list, loader)
    elif construct_type == ConstructType.STAR:
        return _auto_construct_star(node_id_list, loader)
    else:
        raise ValueError("Invalid construct_type.")


def validity_check(
        loader: ObjectLoader,
        network: wgconfig.WireguardNetwork
) -> [bool, str]:
    # entity list check
    c = set()
    for nid in network.node_uuid_list:
        if nid not in loader:
            return False, "Node not found in cache."
        node = loader[nid]
        if not isinstance(node, wgconfig.WireguardNode):
            return False, "Object is not a WireguardNode."
        for cid in node.connection_list:
            c.add(cid)
    for cid in network.connection_uuid_list:
        if cid not in loader:
            return False, "Connection not found in cache."
        connection = loader[cid]
        if not isinstance(connection, wgconfig.WireguardConnection):
            return False, "Object is not a WireguardConnection."
    for cid in c:
        if cid not in network.connection_uuid_list:
            return False, "Connection not found in network."
