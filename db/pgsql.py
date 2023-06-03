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

# 连接到数据库hxy
conn = psycopg2.connect(
    host="localhost",
    port="7777",
    database="postgres",
    user="postgres",
    password="hxy20030620"
)

cur = conn.cursor()

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

# 查询数据示例
cur.execute("""
    SELECT * FROM NodeType
""")
rows = cur.fetchall()
for row in rows:
    print(row)

# 更新数据示例
cur.execute("""
    UPDATE NodeType SET name = 'NEW_NAME' WHERE id = 1
""")

# 删除数据示例
cur.execute("""
    DELETE FROM NodeType WHERE id = 1
""")

# 提交更改并关闭连接
conn.commit()
cur.close()
conn.close()
