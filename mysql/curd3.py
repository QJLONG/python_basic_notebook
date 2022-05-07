import pymysql
from pymysqlpool import *
import uuid
import random
import time

# 创建连接对象
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='hummer',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

config = {
    'pool_name': 'pool',
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'port': 3306,
    'database': 'hummer'
}


def connection_pool():
    pool = ConnectionPool(**config)
    pool.connect()
    return pool

#
def insert1():
    # try:
        with connection_pool().cursor() as cursor:
            # 编写sql
            # email='bjsxt'
            # passwd='1234'
            sql = 'INSERT INTO email(email,password) VALUES'
            for i in range(1000):
                sql += '("'+str(uuid.uuid4())+'",'+'"'+str(random.randint(1000,9999))+'"),'
            sql = sql.rstrip(',')
            print(sql)
            # 执行sql
            result = cursor.execute(sql)
            print('受影响的行数为：{}'.format(result))
            # 提交任务
            connection.commit()
            # 关闭游标
            cursor.close()
    # except Exception as e:
    #     print('操作失败：',e)

def insert2():
    with connection_pool().cursor() as cursor:
        sql = 'INSERT INTO email(email,password) VALUES(%s,%s)'
        l = []
        for i in range(1000):
            data = (str(uuid.uuid4()),str(random.randint(1000,9999)))
            l.append(data)
        result = cursor.executemany(sql,l)
        print('受影响的行数为：',result)
        connection.commit()
        cursor.close()
def main():
    insert2()


if __name__ == '__main__':
    main()
