# -*- coding: utf-8 -*- 
# @Time : 2022/4/12 8:58 
# @Author : hummer 
# @File : practice_1.py

import time

# method 1      time:0.0009276000000000006
# start = time.perf_counter()
# num = 0
# for a in range(1,5):
#     for b in range(1,5):
#         for c in range(1,5):
#             if (a!=b) and (b!=c) and (a!=c):
#                 num = num + 1
#                 print(num , ": " ,a,b,c)
# end = time.perf_counter()
# print("Time counsuming: ",end-start)


# method 2      time:0.0006434000000000023
start = time.perf_counter()
num = 0
list = range(1,5)
for a in list:
    for b in list:
        if b == a:
            continue
        for c in list:
            if (c==a) or (c==b):
                continue
            num = num + 1
            print(num,":",a,b,c)
end = time.perf_counter()
print('Time consuming: ',end-start)