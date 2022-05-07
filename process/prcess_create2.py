from multiprocessing import Process

# 2.通过重写方法创建进程

class MyProcess(Process):

    def __init__(self,num):
        self.num = num
        super().__init__()

    def run(self):
        print('hello',self.num)

if __name__ == '__main__':
    p1 = MyProcess(1)
    p2 = MyProcess(2)
    p1.start()
    p2.start()