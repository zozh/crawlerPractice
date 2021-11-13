def instantiate(func):
    return func()


@instantiate
def next_num():
    a = 0

    def inner():
        nonlocal a
        a += 1
        return a

    return inner


if __name__ == "__main__":
    for i in range(5):
        print(next_num())
