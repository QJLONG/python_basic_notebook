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
    t1.join()
    t2 = threading.Thread(target=game)
    t2.start()
    # t1.join() #t1线程完成之前不会执行主线程
    # t2.join() #t2线程完成之前不会执行主线程
    # listen()
    # game()
    print('我是主线程...')