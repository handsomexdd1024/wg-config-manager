
# 连接到PostgreSQL数据库
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)
# 创建游标对象
cur = conn.cursor()

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
