import inspect
from functools import wraps


def subscriable(func):
    def wrapper(*args, **kwargs):
        if wrapper.subscriptions:
            for c in wrapper.subscriptions:
                c(*args, **kwargs)
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__

    if 'connections' not in wrapper.__dict__:
        wrapper.subscriptions = []
    if 'connect' not in wrapper.__dict__:
        wrapper.subscribe = lambda x: wrapper.subscriptions.append(x)

    return wrapper


def freeze_args(**freezed_kwargs):
    def decorator(func):
        func_spec = inspect.getfullargspec(func)
        args = func_spec.args
        defaults = func_spec.defaults
        kwarg_len = len(defaults) if defaults else 0
        declaration_arguments = []
        call_arguments = []
        for i, a in enumerate(args):
            if a not in freezed_kwargs:
                call_arguments.append(a)
                declaration_arguments.append(a)
            else:
                if i < len(args) - kwarg_len:  # means positional argument
                    call_arguments.append(str(freezed_kwargs[a]))
                else:
                    call_arguments.append(f"{a}={freezed_kwargs[a]}")

        declaration_args = ', '.join(declaration_arguments)
        calling_args = ', '.join(call_arguments)
        print(f"{declaration_args=}")
        print(f"{calling_args=}")

        wrapper_code = f"def wrapper({declaration_args}):\n    return func({calling_args})"
        scope = {}
        exec(wrapper_code, locals(), globals())

        wrapper = globals()["wrapper"]
        wrapper.__name__ = func.__name__

        return wrapper

    return decorator


def on_steroids(func):
    func.freeze = lambda **kwargs: freeze_args(**kwargs)(func)
    func = subscriable(func)
    return func


@on_steroids
def foo(a, b, c):
    print(a, b, c)


foo.subscribe(lambda *args: print("I am subscriber", *args))
foo(1, 2, 3)

short_foo = foo.freeze(a=3)
# short_foo(1, 2)
print(f"{help(short_foo)=}")
