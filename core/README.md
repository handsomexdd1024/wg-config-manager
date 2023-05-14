# `Core`

Core是服务端和客户端共享的核心类和工具模块，包括Wireguard网络节点、网络连接和网络实例的描述类，网络接口的通信格式和转换库等。

- 网络通信的标准格式是json, 所有相关的实现都在这里，client和server的网络模块直接调用即可。

## `wireguard_object.py`

wireguard配置相关描述类。

每个类均实现了`to_json`和`from_json`方法，实现和json的互相转换。

## `user.py`

用户相关描述类。

