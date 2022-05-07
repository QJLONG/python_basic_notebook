import math

# 创建一个判断是否是素数的函数
def isPrime(number):
    # 如果判断的数是2 直接返回真
    if number == 2:
        return True
    # 如果判断的是不是2，则查看是否有可以整除的数
    for i in range(2,int(math.sqrt(number))+1):
        if number % i == 0:
            return False
    return True

# 创建解决问题的函数
def solution(n):
    for number in range(2,n+1):
        # 如果是素数则输出
        if isPrime(number):
            print(number)


def main():
     n = int(input())
     solution(n)

if __name__ == '__main__':
    main()