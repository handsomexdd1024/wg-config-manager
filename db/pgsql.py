import psycopg2
import psycopg2.extras
import uuid
import pickle
from enum import Enum

from core import *


# 枚举类型定义
class NodeType(Enum):
    PEER = 0
    ROUTER = 1
    ROUTED = 2


class EndpointType(Enum):
    IPV4 = 0
    IPV6 = 1
    DOMAIN = 2


# NodeType和EndpointType转换函数
def convert_node_type(node_type):
    return node_type.value


def convert_endpoint_type(endpoint_type):
    return endpoint_type.value


def convert_node_type_back(node_type_value):
    return NodeType(node_type_value)


def convert_endpoint_type_back(endpoint_type_value):
    return EndpointType(endpoint_type_value)


# UUID和字符串转换函数
def convert_uuid_to_str(uuid_obj):
    return str(uuid_obj)


def convert_str_to_uuid(uuid_str):
    return uuid.UUID(uuid_str)


# 列表和字符串转换函数
def convert_list_to_str(lst):
    return ','.join(lst)


def convert_str_to_list(lst_str):
    return lst_str.split(',')


# PEER（Python的序列化格式）和字符串之间的转换
def convert_peer_to_str(peer):
    return pickle.dumps(peer)


def convert_str_to_peer(peer_str):
    return pickle.loads(peer_str)


# UUID和字符串之间的转换
def convert_uuid_to_str(uuid_obj):
    return str(uuid_obj)


def convert_str_to_uuid(uuid_str):
    return uuid.UUID(uuid_str)


# 字节串（bytes）和字符串之间的转换
def convert_bytes_to_str(bytes_obj):
    return bytes_obj.decode('utf-8')


def convert_str_to_bytes(str_obj):
    return str_obj.encode('utf-8')


# 注册类型转换函数
psycopg2.extensions.register_adapter(NodeType, lambda x: x.value)
psycopg2.extensions.register_adapter(EndpointType, lambda x: x.value)
psycopg2.extensions.register_adapter(uuid.UUID, convert_uuid_to_str)
psycopg2.extensions.register_adapter(list, convert_list_to_str)
psycopg2.extensions.register_adapter(bytes, convert_bytes_to_str)
psycopg2.extensions.register_adapter(str, convert_str_to_bytes)
psycopg2.extensions.register_adapter(object, convert_peer_to_str)
psycopg2.extensions.register_adapter(str, convert_str_to_peer)

# 逆向类型转换函数
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
psycopg2.extensions.register_adapter(int, convert_node_type_back)
psycopg2.extensions.register_adapter(int, convert_endpoint_type_back)
psycopg2.extensions.register_adapter(str, convert_str_to_uuid)
psycopg2.extensions.register_adapter(str, convert_str_to_list)

psycopg2.extras.register_uuid()


# 连接到数据库
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="7777",
            database="postgres",
            user="postgres",
            password="hxy20030620"
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to the database:", error)


# 初始化数据库、创建表格和插入数据
def initialize_database():
    conn = connect_to_database()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # 创建表格
        cur.execute("""
            CREATE TABLE IF NOT EXISTS NodeType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ObjectType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS EndpointType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS WireguardNode (
                identifier UUID PRIMARY KEY,
                owner UUID NOT NULL,
                name VARCHAR(50),
                address_list VARCHAR,
                admin_approval BOOLEAN,
                node_type INTEGER REFERENCES NodeType(id),
                private_key VARCHAR,
                public_key VARCHAR,
                endpoint INTEGER REFERENCES EndpointType(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS WireguardObject (
                identifier UUID PRIMARY KEY,
                object_type INTEGER REFERENCES ObjectType(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS WireguardConnection (
                identifier UUID PRIMARY KEY,
                peers VARCHAR,
                preshared_key VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS WireguardNetwork (
                identifier UUID PRIMARY KEY,
                name VARCHAR(50),
                node_uuid_list VARCHAR,
                connection_uuid_list VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_self (
                identifier UUID PRIMARY KEY,
                name VARCHAR(50),
                hashed_password VARCHAR,
                salt VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS WireguardConfig (
                identifier UUID PRIMARY KEY,
                owner UUID,
                name VARCHAR(50),
                address_list VARCHAR,
                network_uuid UUID REFERENCES WireguardNetwork(identifier)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS StandardResponse (
                code INTEGER,
                message VARCHAR,
                content VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS NetworkModification_Action (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS NetworkModification (
                action INTEGER REFERENCES NetworkModification_Action(id),
                content VARCHAR
            )
        """)

        # 插入数据示例
        cur.execute("""
            INSERT INTO NodeType (name) VALUES ('PEER')
        """)
        # 更新数据示例
        cur.execute("""
            UPDATE NodeType SET name = 'NEW_NAME' WHERE id = 1
        """)

        # 删除数据示例
        cur.execute("""
            DELETE FROM NodeType WHERE id = 1
        """)
        conn.commit()
        print("Database initialization and data insertion successful!")
    except (Exception, psycopg2.Error) as error:
        print("Error while initializing database:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 读取数据库并输出数据
def read_from_database():
    conn = connect_to_database()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # 查询数据示例
        cur.execute("""
            SELECT * FROM NodeType
        """)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.Error) as error:
        print("Error while reading from database:", error)

        # NodeType 表查询接口
        def get_node_types():
            conn = psycopg2.connect(
                host="localhost",
                port="7777",
                database="postgres",
                user="postgres",
                password="hxy20030620"
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT * FROM NodeType")  # 执行查询语句
            rows = cur.fetchall()

            node_types = []
            for row in rows:
                node_type = {
                    "id": row["id"],
                    "name": row["name"]
                }
                node_types.append(node_type)

            cur.close()
            conn.close()

            return node_types

        # ObjectType 表查询接口
        def get_object_types():
            conn = psycopg2.connect(
                host="localhost",
                port="7777",
                database="postgres",
                user="postgres",
                password="hxy20030620"
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT * FROM ObjectType")
            rows = cur.fetchall()

            object_types = []
            for row in rows:
                object_type = {
                    "id": row["id"],
                    "name": row["name"]
                }
                object_types.append(object_type)

            cur.close()
            conn.close()

            return object_types

        # EndpointType 表查询接口
        def get_endpoint_types():
            conn = psycopg2.connect(
                host="localhost",
                port="7777",
                database="postgres",
                user="postgres",
                password="hxy20030620"
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT * FROM EndpointType")
            rows = cur.fetchall()

            endpoint_types = []
            for row in rows:
                endpoint_type = {
                    "id": row["id"],
                    "name": row["name"]
                }
                endpoint_types.append(endpoint_type)

            cur.close()
            conn.close()

            return endpoint_types

        # WireguardNode 表查询接口
        def get_wireguard_nodes():
            conn = psycopg2.connect(
                host="localhost",
                port="7777",
                database="postgres",
                user="postgres",
                password="hxy20030620"
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT * FROM WireguardNode")
            rows = cur.fetchall()

            wireguard_nodes = []
            for row in rows:
                wireguard_node = {
                    "identifier": row["identifier"],
                    "owner": row["owner"],
                    "name": row["name"],
                    "oaddress_list": row["oaddress_list"],
                    "admin_approval": row["admin_approval"],
                    "node_type": row["node_type"],
                    "private_key": row["private_key"],
                    "public_key": row["public_key"],
                    "endpoint": row["endpoint"]
                }
                wireguard_nodes.append(wireguard_node)

            cur.close()
            conn.close()

            return wireguard_nodes

        def get_wireguard_networks():
            conn = psycopg2.connect(
                host="localhost",
                port="7777",
                database="postgres",
                user="postgres",
                password="hxy20030620"
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT * FROM WireguardNetwork")
            rows = cur.fetchall()

            wireguard_networks = []
            for row in rows:
                wireguard_network = {
                    "identifier": row["identifier"],
                    "name": row["name"],
                    "node_uuid_list": row["node_uuid_list"],
                    "connection_uuid_list": row["connection_uuid_list"]
                }
                wireguard_networks.append(wireguard_network)

            cur.close()
            conn.close()

            return wireguard_networks
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 调用函数
initialize_database()
read_from_database()
import psycopg2
import psycopg2.extras
import uuid
import pickle
from enum import Enum


# 枚举类型定义
class NodeType(Enum):
    PEER = 0
    ROUTER = 1
    ROUTED = 2


class EndpointType(Enum):
    IPV4 = 0
    IPV6 = 1
    DOMAIN = 2


# 数据库连接和类型转换函数的代码...

# 获取 user_self 表的数据（返回一个 UUID）
def get_user_self(identifier: uuid.UUID) -> user.User:
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        cur.execute("SELECT identifier FROM user_self")
        row = cur.fetchone()

        if row is not None:
            return row[0]  # 返回 UUID

        return None

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching user_self data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取 WireguardConfig 表的数据（返回一个列表）
def get_wireguard_configs(identifiers: list[uuid.UUID]) -> list[wgconfig.WireguardConfig]:
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT identifier FROM WireguardConfig")
        rows = cur.fetchall()

        wireguard_configs = [row[0] for row in rows]  # 返回 UUID 列表
        return wireguard_configs

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching WireguardConfig data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取 WireguardConnection 表的数据（返回一个列表）
def get_wireguard_connections(identifiers: list[uuid.UUID]) -> list[wgobject.WireguardConnection]:
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT identifier FROM WireguardConnection")
        rows = cur.fetchall()

        wireguard_connections = [row[0] for row in rows]  # 返回 UUID 列表
        return wireguard_connections

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching WireguardConnection data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取 WireguardNetwork 表的数据（返回一个列表）
def get_wireguard_networks(identifiers: list[uuid.UUID]) -> list[wgobject.WireguardNetwork]:
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT identifier FROM WireguardNetwork")
        rows = cur.fetchall()

        wireguard_networks = [row[0] for row in rows]  # 返回 UUID 列表
        return wireguard_networks

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching WireguardNetwork data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取 WireguardNode 表的数据（返回一个列表）
def get_wireguard_nodes(identifiers: list[uuid.UUID]) -> list[wgobject.WireguardNode]:
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT identifier FROM WireguardNode")
        rows = cur.fetchall()

        wireguard_nodes = [row[0] for row in rows]  # 返回 UUID 列表
        return wireguard_nodes

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching WireguardNode data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 连接到数据库和初始化的代码...

# 调用函数进行数据查询
user_self = get_user_self()
print("User Self:")
print(user_self)

wireguard_configs = get_wireguard_configs()
print("Wireguard Configs:")
for wireguard_config in wireguard_configs:
    print(wireguard_config)

wireguard_connections = get_wireguard_connections()
print("Wireguard Connections:")
for wireguard_connection in wireguard_connections:
    print(wireguard_connection)

wireguard_networks = get_wireguard_networks()
print("Wireguard Networks:")
for wireguard_network in wireguard_networks:
    print(wireguard_network)

wireguard_nodes = get_wireguard_nodes()
print("Wireguard Nodes:")
for wireguard_node in wireguard_nodes:
    print(wireguard_node)
