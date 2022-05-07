'''
Description: 
Autor: hummer
Date: 2022-04-30 10:45:10
LastEditors: hummer
LastEditTime: 2022-04-30 11:16:12
'''





def return_sum(ls,l,r):
    sum = 0
    for i in ls[l:r]:
        sum += int(i)
    return sum


def group():
    nums = int(input())
    ls = input().split()
    sum = return_sum(ls,0,len(ls))
    
    a = []
    for l in range(len(ls)):
        for r in range(l,len(ls)):
            a.append((l,r))
    flag = 0
    for obj in a:
        if return_sum(ls,obj[0],obj[1]) > sum:
            flag = 1
        break
    
    return flag





num_group = int(input())
flags = []
for i in range(num_group):
    flags.append(group())



for flag in flags:
    if flag == 1:
        print("Yes")
    else:
        print("No")   
