'''
    进程池可以控制同时执行
    的进程的数量（默认为计
    算机处理器个数）
'''

from multiprocessing import Process,Pool
import time
import os

# 创建进程函数
def fun(i):
    time.sleep(1)
    print('Hello %s '%i)
    return "return hello %s "%i

def back(args):
    print(args)


if __name__ == '__main__':
    print('主进程ID：',os.getpid())
    # 创建进程池
    process_pool = Pool() # 默认参数为计算机处理器个数
    for i in range(100):
        # process_pool.apply() # 同步
        process_pool.apply_async(func=fun,args=(i,),callback=back) # 异步 callback参数是进程成功执行之后主进程调用的函数，引用的参数是子进程的返回值

    process_pool.close()
    process_pool.join()

    print('end...')
