'''
    用threading和condition实现红绿灯控
    制十字路口人走车停，人停车走的效果
'''

import threading
import time

# 创建街道类
class Street():

    def __init__(self,condition):
        self._lock = condition
        self.flag = False # 人停车走

    # 设计人走止方法
    def person_southToNorth(self):
        self._lock.acquire()
        if not self.flag:  # 如果flag==False，人等待
            self._lock.wait()
        time.sleep(2)
        print('人南北方向行走。。。。')  # 人走
        self.flag = False
        # 通知其他线程开始执行
        self._lock.notify() 
        self._lock.release()

    # 设计人走车停方法
    def car_eastTowest(self):
        self._lock.acquire()
        # 如果flag==True，车等待
        if self.flag:
            self._lock.wait()
        time.sleep(2)
        print('车东西方向行驶。。。') # 车走
        self.flag = True
        self._lock.notify()
        self._lock.release()


# 创建人类
class Person(threading.Thread):

    def __init__(self,street,name):
        self.street = street

        # 修改线程名称
        super().__init__(name=name)

    # 重写run方法
    def run(self):
        while True:
            self.street.person_southToNorth()

        


# 创建车类
class Car(threading.Thread):

    def __init__(self,street,name):
        self.street = street

        # 修改线程名称
        super().__init__(name=name)

    # 重写run方法
    def run(self):
        while True:
            self.street.car_eastTowest()


if __name__ == '__main__':
    street = Street(threading.Condition())
    person = Person(street,'person')
    car = Car(street,'car')

    person.start()
    car.start()