import pymysql.cursors  # 导入工具

'''
    1. 导入工具 import pymysql.cursors
    2. 创建数据库连接 connection = pymysql.connect('数据库属性信息')
    3. 创建游标对象
    4. 编写sql
    5. 执行sql
        如果是增删改操作，执行cursor.execute(sql,('数据元组'，)),
        如果是查询操作，执行cursoo.execute(sql,('数据元组',)),
    6. 关闭游标对象
    7. 关闭连接
'''

# # 创建数据库连接
# connection = pymysql.connect(
#                             host='localhost',
#                             user='root',
#                             password='root',
#                             db='hummer',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor
#                             )
#
# # 创建游标对象
# try:
#     with connection.cursor() as cursor:
#         # 编写sql
#         sql = 'INSERT INTO stb(name,sex,create_data) VALUES(%s,%s,%s)'
#         # 执行sql
#         result = cursor.execute(sql,('wagnwu','2','2021-09-17 21:04:45.000000'))
#         # 提交事务
#         connection.commit()
#         # 关闭游标对象
#         cursor.close()
#         print('受影响的行数为：',result)
# except Exception as e:
#     print('执行失败，信息为',e)



# # 创建数据库连接
# connnection = pymysql.connect(
#     host = 'localhost',
#     user = 'root',
#     password = 'root',
#     db = 'hummer',
#     charset = 'utf8mb4',
#     cursorclass = pymysql.cursors.DictCursor
# )
#
# # 创建游标对象
# try:
#     with connnection.cursor() as cursor:
#         # 编写sql
#         sql = 'DELETE FROM stb WHERE name=%s'
#         # 执行sql
#         result = cursor.execute(sql,('wagnwu',))
#         # 提交事务
#         connnection.commit()
#         # 关闭游标对象
#         cursor.close()
#         print ('受影响的行数为：',result)
# except Exception as e:
#     print('执行失败，失败原因为：',e)
#


# 创建数据库连接
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='hummer',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# 创建游标对象
try:
    with connection.cursor() as cursor:
        # 编写sql
        sql = 'SELECT name,sex,create_data FROM stb where name=%s'
        # 执行sql
        cursor.execute(sql,('zhangsan',))
        result = cursor.fetchone()
        print(result)
        # 关闭游标对象
        cursor.close()
except Exception as e:
    print('执行失败，失败信息为：',e)


