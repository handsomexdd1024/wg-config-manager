from object_loader import ObjectLoader
from core import *
from uuid import UUID

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

