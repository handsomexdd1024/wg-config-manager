# `数据库设计：`
# `一、wireguard.database:`
## 1.schema WireguardNode:

### (1)table NodeType(Enum和三个int之间的转换)：
- PEER = 0
- ROUTER = 1
- ROUTED = 2
### (2)table EndpointType(Enum和三个int之间的转换):
- IPV4 = 0
- IPV6 = 1
- DOMAIN = 2
### (3)table self
- 包含：name（string）， 
- node_type（PEER与string之间转换）,
- private_key: （string） 
- public_key: （string） 
- endpoint: (string and int)
### (4)table self_address_list:(list与string之间转换）
- [IPv4Address | IPv4Network | IPv6Address | IPv6Network | None]

## 2.schema WireguardConnection(ABC)
### (1)table WireguardConnection.self.
- dentifier:uuid(UUID与string类型的转换)
- peers:uuid(UUID与string类型的转换)
- preshared_key: str | None

## 3.schema WireguardNetwork
### (1)table WireguardNetwork.self.
- dentifier:uuid(UUID与string类型的转换)
- name: string 
- node_list:WireguardNode(list与string类型转换)
- connection_list:WireguardConnection(list与string类型转换)


# `二、user.database`
## 1.schema user_self:
### (1)table user_self
- name（string） 
- identifier(uuid与string类型的转换)
- table self.hashed_password（bytes与string转换） 
- table self.salt（bytes与string转换）