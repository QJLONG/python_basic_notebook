from multiprocessing import Process,Pipe

def child(child_conn):
    print('我是子进程')
    while True:
        try:
            # 子进程通过管道接收主进程发来的信息
            data = child_conn.recv()
            print(data)
        except Exception as e:
            print(e)
            child_conn.close()
            break


def parent(parent_conn):
    print('我是主进程')

    for i in range(10):
        # 主进程通过管道想子进程发送信息
        parent_conn.send(i)


if __name__ == '__main__':
    # 创建双向管道
    parent_conn,child_conn = Pipe()
    # 创建子进程执行child
    p1 = Process(target=child,args=(child_conn,))
    p1.start()

    # 主进程执行parent
    parent(parent_conn)


    parent_conn.close()
    child_conn.close()