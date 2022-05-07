'''
    从终端读取字符串，利用多线程的方法，将字符创转为大写字母并存入文件中
    要求边读边写
'''

import threading
import  time

read_msg = []
save_msg = []


# 读取方法
def _read():
    while True:
        msg = input(">>:")
        if not msg:continue
        read_msg.append(msg)


# 格式化方法
def _format():
    while True:
        if read_msg:
            read_data = read_msg.pop()
            save_msg.append(read_data.upper())


# 写方法
def _write():
    while True:
        if save_msg:
            save_data = save_msg.pop()
            name = "db_"+ time.strftime("%Y_%m_%d_%H_%M_%S")+'.txt'
            print(name)
            with open(name,'w',encoding='utf-8') as f:
                f.write(save_data)



if __name__ == '__main__':
    t1 = threading.Thread(target=_read)
    t1.start()

    t2 = threading.Thread(target=_format)
    t2.start()

    t3 = threading.Thread(target=_write)
    t3.start()