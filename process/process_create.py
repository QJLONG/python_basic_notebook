from multiprocessing import Process
import time

# 1.通过构造器创建进程

def hi(num):
    print('hello',num)

if __name__ == '__main__':

    p1 = Process(target=hi,args=(1,))
    p2 = Process(target=hi,args=(2,))
    p1.start()
    p2.start()
    p1.join()  # 进程执行完再开始主进程  如果有参数，则等待参数时间后便不再等待
    p2.join()
    print('我是主进程。。。')

