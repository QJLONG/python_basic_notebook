# -*- coding: utf-8 -*- 
# @Time : 2022/4/9 17:00 
# @Author : hummer 
# @File : car.py

'''
    1.创建一个animal类用于继承
        属性：种类，名字，年龄
        方法：
    2.创建dog,cat,rabbit类，继承animal类
        属性：owner
        方法：dog（wof~~wof~~~）,cat(miao~~miao~~),rabbit(jump!jump!)
    3.创建hummen类
        属性：name，age
        方法：adopt，walk
'''

# 创建animal类
class Animal(object):
    species = ""
    name = ""
    age = ""

    # 创建构造方法
    def __init__(self,species):
        self.species = species

# 创建dog类
class Dog(Animal):
    owner = ""
    # 创建构造方法
    def __init__(self,name,age):
        super().__init__("dog")
        self.name = name
        self.age = age

    # 设置名字方法
    def set_name(self,new_name):
        self.name = new_name

    # 创建狗叫的方法：
    def dog_action(self):
        if not self.owner:
            print("The Doge is barking:Wof~~Wof~~!!!")
        else:
            print(self.owner + "'s dog is barking:Wof~~Wof~~!!!")

# 创建cat类
class Cat(Animal):
    owner = ""
    # 创建构造方法
    def __init__(self,name,age):
        super().__init__("cat")
        self.name = name
        self.age = age

    # 设置名字方法
    def set_name(self, new_name):
        self.name = new_name

    # 创建猫叫方法
    def cat_action(self):
        if not self.owner:
            print("The cat is meowing:miao~~miao~~!!!")
        else:
            print(self.owner + "'s cat is meowing:miao~~miao~~!")


# 创建hummen类
class Hummen(object):
    name = ""
    age = ""
    # 构造方法
    def __init__(self,name,age):
        self.name = name
        self.age = age

    # 领养方法
    def adopt(self,animal):
        animal.owner = self.name

    # walking方法
    def walk(self,animal):

        if animal.owner != self.name:
            print("The animal is not " + self.name + "'s!!")
        else:
            animal_name = animal.name
            print(self.name + " is walking with his " + animal.species + ": " + animal_name)



if __name__ == '__main__':
    DD = Dog("DD",4)
    DD.dog_action()
    AA = Dog("AA",6)
    Bob = Hummen("Bob",19)
    Bob.adopt(AA)
    Aimy = Hummen("Aimy",18)
    Aimy.adopt(DD)
    Aimy.walk(AA)

