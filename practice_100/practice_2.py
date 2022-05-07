# -*- coding: utf-8 -*- 
# @Time : 2022/4/12 9:23 
# @Author : hummer 
# @File : practice_2.py
import time

profits = int(input("Please input profits >> "))

start = time.perf_counter()

bonus1 = 100000 * 0.1
bonus2 = bonus1 + 100000 * 0.075
bonus3 = bonus2 + 200000 * 0.05
bonus4 = bonus3 + 200000 * 0.03
bonus5 = bonus4 + 400000 * 0.015


if profits <= 100000:
    bonus = profits * 0.1
elif profits <= 200000:
    bonus = bonus1 + (profits-100000) * 0.075
elif profits <=400000:
    bonus = bonus2 + (profits-200000) * 0.05
elif profits <= 600000:
    bonus = bonus3 + (profits-400000) * 0.03
elif profits <=1000000:
    bonus = bonus4 + (profits-600000) * 0.015
else:
    bonus = bonus5 + (profits-1000000) * 0.01

print("bonus: ",bonus)
end = time.perf_counter()
print("Time consuming: ",end-start)