import time
import math


def is_prime(n):
    "判断是否是质数"
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# 装饰器
def display_time(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()
        print(t2 - t1)
        print('call %s():' % func.__name__)

    return wrapper


def find_Prime():
    t1 = time.time()
    for i in range(2, 10000):
        if is_prime(i):
            print(i)
    t2 = time.time()
    print(t2 - t1)


if __name__ == '__main__':
    find_Prime = display_time(find_Prime)
    find_Prime()
    print(find_Prime.__name__)