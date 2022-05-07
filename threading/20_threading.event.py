import threading
import time

class Boss(threading.Thread):

    def run(self):
        print('今晚加班。。。')
        _event.set()        # 将Event()的值设置为True

        time.sleep(3)
        print('下班了，提前休息。。。')
        _event.set()




class Worker(threading.Thread):

    def run(self):
        _event.wait()          # Event()默认值为False 值为False时要等待其他线程将其值改为True
        print('命苦。。。')

        _event.clear()
        _event.wait()
        print('Happy!...')


if __name__ == '__main__':
    _event = threading.Event()
    condition = threading.Condition()

    t1 = Boss()
    t2 = Worker()

    t2.start()
    t1.start()