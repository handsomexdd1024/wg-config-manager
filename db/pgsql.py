import psycopg2

# 连接到PostgreSQL数据库
conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_username",
    password="your_password")

# 创建游标对象
cur = conn.cursor()

# 执行SQL查询
cur.execute("SELECT * FROM your_table")

# 打印查询结果
rows = cur.fetchall()
for row in rows:
    print(row)

# 提交更改并关闭连接
conn.commit()
conn.close()
