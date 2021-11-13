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
def display_time(now_time: str):
    def decorator(func):
        def wrapper():
            t1 = time.time()
            func()
            t2 = time.time()
            print(t2 - t1)
            print(time.strftime("%Y-%m-%d %H:%M:%S", now_time))

        return wrapper

    return decorator


# 被装饰函数
@display_time(time.localtime(time.time()))
# 等价于 find_Prime=display_time(time.localtime(time.time()))(find_Prime)
def find_Prime():
    for i in range(2, 10000):
        if is_prime(i):
            print(i)


if __name__ == '__main__':
    find_Prime()