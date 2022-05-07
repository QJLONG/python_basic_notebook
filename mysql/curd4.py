from pymysql import *
from pymysqlpool import *

# 创建数据库连接
config = {
    'pool_name': 'pool',
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'port': 3306,
    'database': 'hummer'
}

pool = ConnectionPool(**config)


def connect():
    pool.connect()
    print(pool.size)
    return pool


# 创建游标对象
def select_limt(page,row):
    try:
        with connect().cursor() as cursor:
            # 编写sql
            sql = 'SELECT email,password FROM email LIMIT %s,%s'
            cursor.execute(sql,((page-1)*row,row))
            results = cursor.fetchall()
            for result in results:
                print(result)
            cursor.close()
    except Exception as e:
        print('操作失败：',e)

def main():
    page = int(input('请输入page>>'))
    row = int(input('请输入row>>'))
    select_limt(page,row)


if __name__ == '__main__':
    while(True):
        main()