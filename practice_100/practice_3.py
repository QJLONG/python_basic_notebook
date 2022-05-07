# -*- coding: utf-8 -*- 
# @Time : 2022/4/12 9:48 
# @Author : hummer 
# @File : practice_3.py

import math

for i in range(1,100001):
    x = int(math.sqrt(i+100))
    y = int(math.sqrt(i+100+268))
    if (x*x == i+100) and (y*y==i+368):
        print(i)