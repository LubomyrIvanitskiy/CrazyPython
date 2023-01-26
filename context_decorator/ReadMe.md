Using context manager to decorate functions inside

```python

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

foo() # output: I am decorated foo
goo() # output: I am decorated goo
```
