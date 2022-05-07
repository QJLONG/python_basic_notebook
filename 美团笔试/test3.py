'''
Description: 
Autor: hummer
Date: 2022-04-30 10:32:51
LastEditors: hummer
LastEditTime: 2022-04-30 11:33:50
'''

n,m = input().split()
m = int(m)

numbers = input().split()

car_number = 0
for number in numbers:
    number_in = int(number)
    if m+number_in>=0:
        car_number +=1
        m += number_in 
    else:
        car_number=0
    
print(car_number)