# 通过manager对象共享列表和字典资源
from multiprocessing import Process,Manager


def f(d,l,n):
    d[n] = '1'
    l.append(n)
    print(d)
    print(l)
    print(n)


if __name__ == '__main__':
    manager = Manager()
    p_list = []
    d = manager.dict()
    l = manager.list(range(5))
    for i in range(5):
        p = Process(target=f,args=(d,l,i))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()