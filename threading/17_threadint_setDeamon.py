import threading
import time

def listen():
    print('begin to listen to music',time.strftime("%X"))
    time.sleep(3)
    print("end to listen to music",time.strftime("%X"))

def game():
    print('begin to play game',time.strftime("%X"))
    time.sleep(5)
    print('end to play game',time.strftime("%X"))

if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t1.start()

    # 判断线程是否是活动的
    print(t1.is_alive())

    # 返回线程名称
    print(t1.getName())

    # 修改线程名称
    t1.setName('threading_1')
    print(t1.getName())

    # 返回当前线程对象
    print(threading.current_thread())

    # 返回正在运行的线程list
    print(threading.enumerate())

    # 返回正在运行的线程数量
    print(threading.active_count())

    # 返回当前线程ID
    print(threading.get_ident())

    t2 = threading.Thread(target=game)
    # 守护线程：随主线程退出而退出
    t2.setDaemon(True)  # 将该子线程设置为主线程的守护线程  写在该线程的start方法之前才会生效
    t2.start()
    print('我是主线程...')