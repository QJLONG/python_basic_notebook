# 互斥锁（同步锁）  用来对共享资源的同步访问

import threading
import time


def add():
    # 让锁内的代码同步执行，锁住拿到的资源不让其被其他线程共享
    _lock.acquire()     # 加锁
    global  num
    temp = num
    time.sleep(0.01)
    num = temp + 1
    _lock.release()     # 释放锁



if __name__ == '__main__':

    # 创建同步锁对象
    _lock = threading.Lock()
    num = 0

    l = []

    for i in range(100):
        t = threading.Thread(target=add)
        t.start()
        l.append(t)

    for t in l:
        t.join()


    print(num)
