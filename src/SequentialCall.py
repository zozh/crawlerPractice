call_table = list()


def sequential_call(prefix: str = None):
    def decorator(func):
        def wrapper():
            call_table.append(func.__name__)
            if prefix == None:
                pass
            elif not prefix in call_table:
                raise ValueError("调用顺序错误")
            func()

        return wrapper

    return decorator


@sequential_call()
def database():
    print("database")


@sequential_call("database")
def table():
    print("table")


@sequential_call("table")
def crud():
    print("crud")


# 调用顺序a->b->c，不然抛出错误
if __name__ == "__main__":
    # database()
    # table()
    crud()
