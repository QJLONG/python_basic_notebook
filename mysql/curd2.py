from pymysql import  *

# 创建数据库连接
connection = connect(
    host='localhost',
    user='root',
    password='root',
    db='hummer',
    charset='utf8mb4',
    cursorclass=cursors.DictCursor
)

# 创建插入方法
def create(name,sex,create_data):
    # 创建游标对象
    try:
        with connection.cursor() as cursor:
            # -------------方法一----------------
            # 编辑sql
            sql = 'INSERT INTO stb(name,sex,create_data) VALUES(%s,%s,%s)'
            # 执行sql
            result = cursor.execute(sql,(name,sex,create_data))

            # --------------方法二--------------
            #sql = 'INSERT INTO stb(name,sex,create_data) VALUES("'+name+'","'+sex+'","'+create_data+'")'
            #result = cursor.execute(sql)
            print('受影响的函数为：',result)
            # 提交任务
            connection.commit()
            # 关闭游标
            cursor.close()
    except Exception as e:
        print('操作失败：',e)

# 创建删除方法
def delete(name):
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM stb WHERE name=%s'
            result = cursor.execute(sql,(name,))
            print('受影响的行数为：',result)
            connection.commit()
            cursor.close()
    except Exception as e:
        print('操作失败：',e)


# 创建查询方法
def query(name):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM stb WHERE name=%s'
            cursor.execute(sql,(name,))
            result = cursor.fetchone()
            print(result)
            cursor.close()
    except Exception as e:
        print('操作失败：',e)

# 创建查询多条数据方法
def querymany(sex):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM stb WHERE sex=%s'
            cursor.execute(sql,(sex,))
            result = cursor.fetchall()
            print(result)
            cursor.close()
    except Exception as e:
        print('操作失败：',e)



def main():
    # name = input('请输入姓名>>')
    sex = input('请输入性别>>')
    # create_data = '2021-09-17 21:27:44.000000'
    # create(name,sex,create_data)
    # delete(name)
    querymany(sex)
if __name__ == '__main__':
    main()