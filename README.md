# 中心化WireGuard配置文件管理服务器

2023年软工Python课设小组作业。

## 基本功能

- 将Wireguard节点可视化展示并提供操作接口。
- 实时根据路由表展示节点路由情况，支持Peer to Peer和Router-Client式路由。
- 支持IPv6 ULA与IPv6 LLA自动生成与创建。
- 普通用户可以一键下载本节点配置文件，并上传自己的公钥信息等待批准。
- 管理员可以修改所有配置并批准终端用户的身份信息。

## 项目模块

### 前端

- 可视化展示
- 可视化配置
- 用户登录界面

### 业务逻辑

- WireGuard节点类
- wg网络架构的描述类
- 配置文件的生成和修改
- 用户身份验证和鉴权

### 外部工具交互

- 网络通信模块
- 数据库交互模块
- TLS和身份验证所用的密码学库
- WireGuard密钥生成
- yaml库和toml库

## Acknowledgement

Copyright (c) 2023 Billy Yang, Jayson Luo, Kathrine Hu.

本项目以GNU AGPLv3协议开源。

本项目使用了以下开源项目的代码：

- [Python3](https://www.python.org/) (PSFL License)
- [wireguard-tools (Python implementation)](https://github.com/cmusatyalab/wireguard-tools) (MIT License)
- [PyYAML](https://github.com/yaml/pyyaml) (MIT License)
- [bcrypt](https://github.com/pyca/bcrypt) (Apache License 2.0)
- [Psycopg](https://www.psycopg.org) (GNU LGPLv3)

本小组成员在此对以上项目的开发者表示感谢。