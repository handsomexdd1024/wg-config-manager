import ipaddress

import wireguard_tools

import wgobject
import uuid
import msgpack

n = wgobject.WireguardNode(
    identifier=uuid.uuid4(),
    owner=uuid.uuid4(),
    name="test",
    address_list=[
        ipaddress.IPv4Address("192.168.1.1")
    ],
    private_key=wireguard_tools.WireguardKey.generate(),
    endpoint=("router.xiaodiandong.xyz", 12345)
)
print(n.uuid)

p = msgpack.packb(n, use_bin_type=True, default=wgobject.WireguardNode.default_encoder)
print(p)

e = msgpack.unpackb(p, raw=False, object_hook=wgobject.WireguardNode.default_decoder)
assert isinstance(e, wgobject.WireguardNode)
print(e.uuid)
