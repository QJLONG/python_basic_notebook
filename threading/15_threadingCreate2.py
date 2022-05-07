import threading

class MyThread(threading.Thread):

    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num

    def hi(self):
        print('hello %s' % self.num)

    def run(self):
        self.hi()


if __name__ == '__main__':
    t1 = MyThread(10)
    t1.start()

    t2 = MyThread(9)
    t2.start()

    print('我是主线程。。。')