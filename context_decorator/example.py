from context_decorator import decorator


def my_decor(func):
    def wrapper(*args, **kwargs):
        print("I am decorated", func.__name__)
        return func(*args, **kwargs)

    return wrapper


with decorator(my_decor):
    def foo():
        pass


    def goo():
        pass

foo()
goo()
