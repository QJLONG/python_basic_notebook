'''
Description: 
Autor: hummer
Date: 2022-04-30 10:10:24
LastEditors: hummer
LastEditTime: 2022-04-30 14:12:32
'''
s = input()
t = input()


sum_str = 0
length = len(s)
for i in range(len(t)-length+1):
    sub_str = t[i:i+length]
    for j in range(length):
        sum_str += abs(int(sub_str[j])-int(s[j]))

print(sum_str)
