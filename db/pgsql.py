import psycopg2
from psycopg2.extras import Json

# 连接到数据库
conn = psycopg2.connect(
    host="localhost",
    port="7777",
    database="postgres",
    user="postgres",
    password="hxy20030620"
)
cur = conn.cursor()
# 创建 schema 和 table
def create_schema_and_tables():
    try:
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

        # 提交事务
        conn.commit()

        print("Schema and tables created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating schema and tables:", error)

# 插入数据示例
def insert_data():
    try:
        identifier = "e6b021d1-9b0a-4a9b-a684-6d70b9f4a7c9"  # 示例 identifier
        name = "John"  # 示例 name
        address_list = ["192.168.0.1", "192.168.0.2"]  # 示例 address_list

        # 转换数据格式
        address_list_json = Json(address_list)

        # 插入数据
        cur.execute("""
            INSERT INTO wireguard.self (identifier, name, address_list)
            VALUES (%s, %s, %s)
        """, (identifier, name, address_list_json))

        # 提交事务
        conn.commit()

        print("Data inserted successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data:", error)

# 获取数据示例
def retrieve_data():
    try:
        cur.execute("SELECT * FROM wireguard.self")
        rows = cur.fetchall()

        for row in rows:
            identifier = row[0]
            name = row[1]
            address_list_json = row[2]

            # 转换数据格式
            address_list = address_list_json['{']  # 示例转换方式，请根据实际存储方式进行调整

            # 打印数据
            print("Identifier:", identifier)
            print("Name:", name)
            print("Address List:", address_list)

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving data:", error)

# 创建数据库、模式和表格
create_schema_and_tables()

# 插入数据示例
insert_data()

# 获取数据示例
retrieve_data()

# 关闭连接
cur.close()
conn.close()