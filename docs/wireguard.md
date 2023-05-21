# Wireguard相关业务逻辑

## 网络配置

配置本身维护以下信息：

- id
- name
- owner
- user_list
- network_uuid

### 网络节点

node维护以下信息：

- id
- 名称
- 是否获得管理员批准
- 节点类型
  - peer: 普通节点，以wireguard连接到该网络
  - router: 路由器，允许其他设备通过该设备转发流量到wireguard网络
  - routed: 由路由器路由的节点
- ip信息
  - peer & router: ipv4 address & ipv6 address
  - router & routed: ipv4 network & ipv6 network
  - 如果是router类型，额外维护允许路由的列表
- 公钥
- 私钥
  - **出于安全考虑，私钥可以不上传到服务端**
- owner
- 公网端点：(ip, port)
- create_route: 是否创建路由规则

限制：

- routed节点没有公钥（因为不需要配置网络）
- 只有router允许拥有非/32或/128的ip
- router和routed节点所使用的子网不允许冲突
- routed节点没有公钥

### 网络连接

connection维护以下信息：

- id
- 连接的节点信息
- pre-shared key

限制：

- 边不能连接两个routed object
- 如果连接了一个peer/router与一个routed device, 则pre-shared key不适用

### 完整网络

网络维护以下信息：

- id
- name
- node_list
- connection_list

## 自动构建网络

- 没有public endpoint的设备需要通过路由访问网络
- full mesh的所有peer必须都具有public endpoint

### 路由网络

选择恰好一个带public-endpoint的节点和多个没有公网端口的节点，构建路由规则

### Full-Mesh 网络

选择多个带公网端口的节点，两两建边