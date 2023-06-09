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
            host='localhost',
            port=7777,
            database='postgres',
            user='postgres',
            password='hxy20030620'
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("连接到数据库时发生错误:", error)


# 初始化数据库、创建表格和插入数据
def initialize_database():
    conn = connect_to_database()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        #创建必要的schema和schema下对应的表
        # 创建 schema WireguardNode
        cur.execute("""
                    CREATE SCHEMA IF NOT EXISTS wireguard
                """)

        # 创建 table NodeType
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguard.NodeType (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255)
                    )
                """)

        # 创建 table EndpointType
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguard.EndpointType (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255)
                    )
                """)

        # 创建 table self
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguard.self (
                        identifier UUID PRIMARY KEY,
                        owner UUID,
                        name VARCHAR(255),
                        address_list JSONB,
                        admin_approval BOOLEAN,
                        node_type VARCHAR(255),
                        private_key TEXT,
                        public_key TEXT,
                        endpoint TEXT
                    )
                """)

        # 创建 schema WireguardObject
        cur.execute("""
                    CREATE SCHEMA IF NOT EXISTS wireguardobject
                """)

        # 创建 table ObjectType
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguardobject.ObjectType (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255)
                    )
                """)

        # 创建 table self
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguardobject.self (
                        identifier UUID PRIMARY KEY,
                        object_type INTEGER
                    )
                """)

        # 创建 schema WireguardConnection
        cur.execute("""
                    CREATE SCHEMA IF NOT EXISTS wireguardconnection
                """)

        # 创建 table self
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguardconnection.self (
                        identifier TEXT PRIMARY KEY,
                        peers TEXT,
                        preshared_key TEXT
                    )
                """)

        # 创建 schema WireguardNetwork
        cur.execute("""
                    CREATE SCHEMA IF NOT EXISTS wireguardnetwork
                """)

        # 创建 table self
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wireguardnetwork.self (
                        identifier TEXT PRIMARY KEY,
                        name VARCHAR(255),
                        node_uuid_list TEXT,
                        connection_uuid_list TEXT
                    )
                """)
        # 在public schema中创建12个表，包含全部范围
        cur.execute("""
            CREATE TABLE NodeType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE EndpointType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE ObjectType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE WireguardNode (
                identifier UUID PRIMARY KEY,
                owner UUID NOT NULL,
                name VARCHAR(50),
                oaddress_list VARCHAR,
                admin_approval BOOLEAN,
                node_type INTEGER REFERENCES NodeType(id),
                private_key VARCHAR,
                public_key VARCHAR,
                endpoint INTEGER REFERENCES EndpointType(id)
            )
        """)

        cur.execute("""
            CREATE TABLE WireguardObject (
                identifier UUID PRIMARY KEY,
                object_type INTEGER REFERENCES ObjectType(id)
            )
        """)

        cur.execute("""
            CREATE TABLE WireguardConnection (
                identifier UUID PRIMARY KEY,
                opeers VARCHAR,
                preshared_key VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE WireguardNetwork (
                identifier UUID PRIMARY KEY,
                name VARCHAR(50),
                node_uuid_list VARCHAR,
                connection_uuid_list VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE user_self (
                identifier UUID PRIMARY KEY,
                name VARCHAR(50),
                hashed_password VARCHAR,
                salt VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE WireguardConfig (
                identifier UUID PRIMARY KEY,
                owner UUID,
                name VARCHAR(50),
                address_list VARCHAR,
                network_uuid UUID REFERENCES WireguardNetwork(identifier)
            )
        """)

        cur.execute("""
            CREATE TABLE StandardResponse (
                code INTEGER,
                message VARCHAR,
                content VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE NetworkModification_Action (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE NetworkModification (
                action INTEGER REFERENCES NetworkModification_Action(id),
                content VARCHAR
            )
        """)
        # 提交事务
        conn.commit()

        print("Schema and tables created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating schema and tables:", error)

        # 插入数据示例
        cur.execute(
            "INSERT INTO NodeType (name) VALUES ('PEER')"
        )
        # 更新数据示例
        cur.execute(
            "UPDATE NodeType SET name = 'NEW_NAME' WHERE id = 1"
        )

        # 删除数据示例
        cur.execute(
            "DELETE FROM NodeType WHERE id = 1"
        )
        conn.commit()
        print("数据库初始化和数据插入成功!")
    except (Exception, psycopg2.Error) as error:
        print("初始化数据库时发生错误:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 读取数据库并输出数据
def get_user_self(identifier):
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT * FROM user_self WHERE identifier = %s", (identifier,))
        row = cur.fetchone()

        if row is not None:
            # todo: 对提取出的数据进行类型转换
            user_self = {
                'identifier': convert_str_to_uuid(row['identifier']),  # 比如这里的identifier是UUID类型，但是从数据库中提取出来不是UUID类型，需要转换
                'name': row['name'],  # 其余字段类似
                'hashed_password': row['hashed_password'],
                'salt': row['salt']
            }
            return user_self

        return None
    except (Exception, psycopg2.Error) as error:
        print("获取用户信息时发生错误:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 转换identifiers列表中的UUID为字符串类型
def convert_uuid_list_to_str(identifiers):
    return [str(identifier) for identifier in identifiers]


# 获取WireguardConfig对象
def get_wireguard_config(identifier):
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT * FROM WireguardConfig WHERE identifier = %s", (identifier,))
        row = cur.fetchone()

        if row is not None:
            wireguard_config = {
                'identifier': convert_str_to_uuid(row['identifier']),
                'owner': row['owner'],
                'name': row['name'],
                'address_list': row['address_list'],
                'network_uuid': row['network_uuid']
            }
            return wireguard_config

        return None
    except (Exception, psycopg2.Error) as error:
        print("获取WireguardConfig对象时发生错误:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取WireguardConnection对象列表
def get_wireguard_connections(identifiers):
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        identifiers_str = convert_uuid_list_to_str(identifiers)
        cur.execute("SELECT * FROM WireguardConnection WHERE identifier = ANY(%s)", (identifiers_str,))
        rows = cur.fetchall()

        wireguard_connections = []
        for row in rows:
            wireguard_connection = {
                'identifier': convert_str_to_uuid(row['identifier']),
                'peers': row['peers'],
                'preshared_key': row['preshared_key']
            }
            wireguard_connections.append(wireguard_connection)

        return wireguard_connections
    except (Exception, psycopg2.Error) as error:
        print("获取WireguardConnection对象列表时发生错误:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取WireguardNetwork对象列表
def get_wireguard_networks(identifiers):
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        identifiers_str = convert_uuid_list_to_str(identifiers)
        cur.execute("SELECT * FROM WireguardNetwork WHERE identifier = ANY(%s)", (identifiers_str,))
        rows = cur.fetchall()

        wireguard_networks = []
        for row in rows:
            wireguard_network = {
                'identifier': convert_str_to_uuid(row['identifier']),
                'name': row['name'],
                'node_uuid_list': row['node_uuid_list'],
                'connection_uuid_list': row['connection_uuid_list']
            }
            wireguard_networks.append(wireguard_network)

        return wireguard_networks
    except (Exception, psycopg2.Error) as error:
        print("获取WireguardNetwork对象列表时发生错误:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 获取WireguardNode对象列表
def get_wireguard_nodes(identifiers):
    conn = connect_to_database()
    if conn is None:
        return None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        identifiers_str = convert_uuid_list_to_str(identifiers)
        cur.execute("SELECT * FROM WireguardNode WHERE identifier = ANY(%s)", (identifiers_str,))
        rows = cur.fetchall()

        wireguard_nodes = []
        for row in rows:
            wireguard_node = {
                'identifier': convert_str_to_uuid(row['identifier']),
                'owner': row['owner'],
                'name': row['name'],
                'address_list': row['address_list'],
                'admin_approval': row['admin_approval'],
                'node_type': row['node_type'],
                'private_key': row['private_key'],
                'public_key': row['public_key'],
                'endpoint': row['endpoint']
            }
            wireguard_nodes.append(wireguard_node)

        return wireguard_nodes
    except (Exception, psycopg2.Error) as error:
        print("获取WireguardNode对象列表时发生错误:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 测试代码:
def test_code():
    user_identifier = uuid.UUID('your_user_identifier')
    wireguard_config_identifier = uuid.UUID('your_wireguard_config_identifier')
    wireguard_connection_identifiers = [
        uuid.UUID('connection_identifier_1'),
        uuid.UUID('connection_identifier_2')
    ]
    wireguard_network_identifiers = [
        uuid.UUID('network_identifier_1'),
        uuid.UUID('network_identifier_2')
    ]
    wireguard_node_identifiers = [
        uuid.UUID('node_identifier_1'),
        uuid.UUID('node_identifier_2')
    ]

    user_self = get_user_self(user_identifier)
    print(user_self)

    wireguard_config = get_wireguard_config(wireguard_config_identifier)
    print(wireguard_config)

    wireguard_connections = get_wireguard_connections(wireguard_connection_identifiers)
    for connection in wireguard_connections:
        print(connection)

    wireguard_networks = get_wireguard_networks(wireguard_network_identifiers)
    for network in wireguard_networks:
        print(network)

    wireguard_nodes = get_wireguard_nodes(wireguard_node_identifiers)
    for node in wireguard_nodes:
        print(node)


# 执行测试代码:将对应的uuid.UUID替换后，去掉下一行的注释可以进行执行测试代码
#test_code()
