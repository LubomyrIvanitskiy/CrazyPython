class structure:

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            args = [key,]
        else:
            args = key
        args = list(args)
        kwargs = {}
        for i in range(len(args)-1, -1, -1):
            a = args[i]
            if isinstance(a, slice):
                kwargs[a.start] = a.stop
                del args[i]
        return self.__call__(*args, **kwargs)


@structure
def foo(x: int):
    return x


print(foo[9])
