import threading
import time

# 通过thread构造器创建线程

def hi(num):
    print('hello %s' % num)
    time.sleep(3)


if __name__ == '__main__':
    # hi(10)
    t = threading.Thread(target=hi,args=(10,)) # 创建线程对象(子线程)
    t1 = threading.Thread(target=hi,args=(9,)) # 创建线程对象(子线程)
    t.start()
    t1.start()

    print('我是主线程...')