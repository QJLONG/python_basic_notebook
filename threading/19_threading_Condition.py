'''
    用threading_conditon实现模拟街道红绿灯下的人走车停
'''

import threading
import time

# 创建街道类
class Street():
    def __init__(self,condition):
        self.flag = False
        self.condition = condition

    # 创建人行走方法 flag=True 可以南北同行，flag=False等待
    def person_run(self):
        # 加锁
        self.condition.acquire()
        if not self.flag:
            # 等待
            self.condition.wait()
        # 人开始南北行走
        print('People are walking from south to north...')
        time.sleep(2)
        self.flag = False
        # 通知其他程序开始获取资源
        self.condition.notify()
        # 释放资源
        self.condition.release()

    # 创建汽车行驶方法 flag=Ture 汽车开始行驶，flag=False 汽车等待
    def car_run(self):
        # 加锁
        self.condition.acquire()
        if self.flag:
            # 汽车等待人走完
            self.condition.wait()
        # 汽车开始东西方向行驶
        print('Cars are running from east to west..')
        time.sleep(2)
        self.flag=True
        # 通知其他线程开始调用临界资源
        self.condition.notify()
        # 释放资源
        self.condition.release()

# 创建人类
class Person(threading.Thread):
    def __init__(self,street,name):
        self.street = street
        # 重写线程名
        super().__init__(name=name)

    # 重写run方法
    def run(self):
        while True:
            self.street.person_run()

# 创建汽车类
class Car(threading.Thread):
    def __init__(self,street,name):
        self.street = street
        # 重写线程名
        super().__init__(name=name)

    # 重写run方法
    def run(self):
        while True:
            self.street.car_run()


if __name__ == '__main__':
    street = Street(threading.Condition())
    person = Person(street,'people')
    car = Car(street,'cars')
    person.start()
    car.run()






# # 创建加法方法
# def add():
#     _lock.acquire()
#     global num1
#     print("num1:",num1)
#     temp = num1
#     num1 = temp +1
#     time.sleep(0.1)
#     _lock.release()
#
# # 创建减法方法
# def sub():
#     _lock.acquire()
#     global num2
#     print("num2:",num2)
#     temp = num2
#     num2 = temp - 1
#     time.sleep(0.01)
#     _lock.release()
#
#
# if __name__ == '__main__':
#     num1 = 0
#     num2 = 100
#     time1 = time.time()
#     _lock = threading.Condition()
#     for i in range(100):
#         t1 = threading.Thread(target=add)
#         t2 = threading.Thread(target=sub)
#         t1.start()
#         t2.start()
#
#     time.sleep(2)
#     print('time',time.time() - time1)

