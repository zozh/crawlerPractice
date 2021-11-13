def sequential_call(read_write="read"):
    def sequential_call_fun(func):
        def sequential(*args, **kwargs):
            pass