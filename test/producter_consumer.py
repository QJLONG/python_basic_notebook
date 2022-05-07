import threading
import time
import queue

# 创建生产面包方法
def create_bread(name):
    count = 1
    while True:
        print('生产者%s正在生产第%s个面包。。。'%(name,count))
        time.sleep(3)
        bread_queue.put(count)
        print('生产者%s已经完成了第%s个面包！'%(name,count))
        count += 1

# 创建消费者吃面包方法
def eat_bread(name):
    count = 1
    while True:
        time.sleep(5)
        if not bread_queue.empty():
            print('消费者%s正在享受第%s个面包。。。'%(name,count))
            bread_queue.get()
        else:
            print('面包已经卖完了，请稍等。。。')

        count += 1


if __name__ == '__main__':
    bread_queue = queue.Queue()
    producter1 = threading.Thread(target=create_bread,args=('A',))
    producter2 = threading.Thread(target=create_bread,args=('B',))

    consumer1 = threading.Thread(target=eat_bread,args=('A',))
    consumer2 = threading.Thread(target=eat_bread, args=('B',))
    consumer3 = threading.Thread(target=eat_bread, args=('C',))
    producter1.start()
    producter2.start()
    consumer1.start()
    time.sleep(2)
    consumer2.start()
    time.sleep(2)
    consumer3.start()
