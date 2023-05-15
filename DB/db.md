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
### (3)self
### (1)table self.name（string）
### (2)table self.identifier(uuid与string类型的转换)
           
# 二、user.database
## 1.schema user_self:
### (1)table self.name（string）
### (2)table self.identifier(uuid与string类型的转换)
### (3)table self.hashed_password（bytes与string转换）
### (4)table self.salt（bytes与string转换）