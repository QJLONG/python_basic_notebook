import threading
import time


# 创建street类
class Street:

    # 初始化方法
    def __init__(self,conidition):
        self.condition = conidition
        self.flag = True # Ture代表人走车停 False代表人停车走


    # 人行走方法
    def person_run(self):
        # 加锁
        self.condition.acquire()

        # 如果flag==False 人等待
        if not self.flag:
            self.condition.wait()
        # 人开始行走
        print('People are running from South to North....')
        time.sleep(2)
        self.flag = False

        # 通知car开始行驶
        self.condition.notify()
        # 解锁
        self.condition.release()

    # 车行驶方法
    def car_run(self):
        # 加锁
        self.condition.acquire()

        # 如果falg==Ture 车停人走
        if self.flag:
            self.condition.wait()

        # 车开始行驶
        print('Cars are running from East to West....')
        time.sleep(2)
        self.flag = True
        # 通知人开始行驶
        self.condition.notify()
        # 解锁
        self.condition.release()


# 创建人类
class Person(threading.Thread):
    # 初始化方法
    def __init__(self,street,name):
        self.street = street

        # 重写线程名
        super().__init__(name = name)

    # 行驶方法
    def run(self):
        while True:
            self.street.person_run()


# 创建车类
class Car(threading.Thread):
    # 初始化方法
    def __init__(self,street,name):
        self.street = street
        # 重写线程名
        super().__init__(name = name)

    # 行驶方法
    def run(self):
        while True:
            self.street.car_run()


if __name__ == '__main__':
    condition = threading.Condition()
    street = Street(condition)
    t1 = Person(street,'People')
    t2 = Car(street,'Cars')
    t1.start()
    t2.start()

