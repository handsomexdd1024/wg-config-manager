
# 连接到Postgres数据库
import psycopg

conn = psycopg.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)
# 创建游标对象
cur = conn.cursor()
# 创建数据库
def create_database():
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE wireguard")
        cursor.close()
        conn.commit()
        print("Database created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating database:", error)

# 创建模式
def create_schema():
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE SCHEMA wireguard")
        cursor.close()
        conn.commit()
        print("Schema created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating schema:", error)

# 创建表格
def create_tables():
    try:
        cursor = conn.cursor()
        # 创建schema WireguardNode下的表格 NodeType
        cursor.execute("""
            CREATE TABLE wireguard.NodeType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            )
        """)

        # 创建schema WireguardNode下的表格 EndpointType
        cursor.execute("""
            CREATE TABLE wireguard.EndpointType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            )
        """)

        # 创建schema WireguardNode下的表格 self
        cursor.execute("""
            CREATE TABLE wireguard.self (
                identifier UUID PRIMARY KEY,
                owner UUID,
                name VARCHAR(255),
                address_list TEXT,
                admin_approval BOOLEAN,
                node_type VARCHAR(255),
                private_key TEXT,
                public_key TEXT,
                endpoint TEXT
            )
        """)

        # 创建schema WireguardObject下的表格 ObjectType
        cursor.execute("""
            CREATE TABLE wireguard.ObjectType (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            )
        """)

        # 创建schema WireguardObject下的表格 self
        cursor.execute("""
            CREATE TABLE wireguard.self (
                identifier UUID PRIMARY KEY,
                object_type INTEGER
            )
        """)

        # 创建schema WireguardConnection下的表格 self
        cursor.execute("""
            CREATE TABLE wireguard.self (
                identifier TEXT PRIMARY KEY,
                peers TEXT,
                preshared_key TEXT
            )
        """)

        # 创建schema WireguardNetwork下的表格 self
        cursor.execute("""
            CREATE TABLE wireguard.self (
                identifier TEXT PRIMARY KEY,
                name VARCHAR(255),
                node_uuid_list TEXT,
                connection_uuid_list TEXT
            )
        """)

        cursor.close()
        conn.commit()
        print("Tables created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating tables:", error)

# 创建数据库、模式和表格
create_database()
create_schema()
create_tables()
#提交和回滚事务

try:
    # 执行多个SQL操作
    cur.execute("INSERT INTO mytable (name) VALUES ('John')")
    cur.execute("UPDATE mytable SET age = 30 WHERE name = 'John'")

    # 提交事务
    conn.commit()
except:
    # 发生错误时回滚事务
    conn.rollback()

# 关闭游标
cur.close()

#执行SQL语句：使用连接对象的cursor()方法创建游标对象，然后使用游标对象的execute()方法执行SQL语句
# 创建游标对象
cur = conn.cursor()

# 执行SQL查询
cur.execute("SELECT * FROM mytable")

# 获取查询结果
rows = cur.fetchall()

# 处理查询结果
for row in rows:
    print(row)

# 关闭游标
cur.close()

# 执行SQL查询
cur.execute("SELECT * FROM your_table")

# 获取查询结果
rows = cur.fetchall()

# 处理查询结果
for row in rows:
    print(row)

# 打印查询结果
rows = cur.fetchall()
for row in rows:
    print(row)

# 提交更改并关闭连接
conn.commit()
conn.close()
