import collections
import functools
import inspect


def para_check(func):
    """
    函数参数检查装饰器，需要配合函数注解表达式（Function Annotations）使用
    """
    msg = 'Argument {argument} must be {expected!r},but got {got!r},value {value!r}'

    # 获取函数定义的参数
    sig = inspect.signature(func)
    parameters = sig.parameters  # 参数有序字典
    arg_keys = tuple(parameters.keys())  # 参数名称

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        CheckItem = collections.namedtuple('CheckItem',
                                           ('anno', 'arg_name', 'value'))
        check_list = []

        # collect args   *args 传入的参数以及对应的函数参数注解
        for i, value in enumerate(args):
            arg_name = arg_keys[i]
            anno = parameters[arg_name].annotation
            check_list.append(CheckItem(anno, arg_name, value))

        # collect kwargs  **kwargs 传入的参数以及对应的函数参数注解
        for arg_name, value in kwargs.items():
            anno = parameters[arg_name].annotation
            check_list.append(CheckItem(anno, arg_name, value))

        # check type
        for item in check_list:
            if not isinstance(item.value, item.anno):
                error = msg.format(expected=item.anno,
                                   argument=item.arg_name,
                                   got=type(item.value),
                                   value=item.value)
                raise TypeError(error)

        return func(*args, **kwargs)

    return wrapper


call_table = list()


def sequential_call(prefix: str = None):
    """函数调用顺序限制

    Args:
        prefix (str): 前置函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            call_table.append(func.__name__)
            if prefix == None:
                pass
            elif not prefix in call_table:
                raise ValueError("调用顺序错误")
            func(*args, **kwargs)

        return wrapper

    return decorator
