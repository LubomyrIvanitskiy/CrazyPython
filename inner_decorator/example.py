from inner_decorator import inner_decorator


def cal_reporting(func):
    def wrapper(*args, **kwargs):
        print(func.__name__, args, kwargs, "is called")
        return func(*args, **kwargs)

    return wrapper


def my_print(*args, **kwargs):
    for i in range(3):
        print(*args, **kwargs)


@inner_decorator(
    f1=cal_reporting,
    f2=cal_reporting,
    print=lambda _: my_print
)
def random_outer_func():
    def f1():
        pass

    def f2(a, b):
        return a + b

    f1()
    f2(2, 2)
    print("hello")

random_outer_func()