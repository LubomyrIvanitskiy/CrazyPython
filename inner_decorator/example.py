import time
from functools import wraps

from inner_decorator import inner_decorator


def my_print(*args, **kwargs):
    for i in range(3):
        print(*args, **kwargs)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


@inner_decorator(
    timeit,
    print=lambda _: my_print
)
def random_outer_func():
    def f1():
        pass

    def f2(a, b):
        return a + b

    f1()
    f2(2, 2)
    print("Good Bye")


random_outer_func()
