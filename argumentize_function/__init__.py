import builtins
import inspect
from collections import ChainMap
from functools import wraps


def argumentize(func):
    context = ChainMap(
        vars(builtins),
        func.__globals__
    )
    gl = {k: context[k] for k in func.__code__.co_names}
    original_globals = dict(**gl)
    original_closure_vals = []
    original_arg_names = inspect.getfullargspec(func).args

    new_func = type(func)(func.__code__, gl, name=func.__name__,
                          argdefs=inspect.getfullargspec(func).defaults,
                          closure=func.__closure__)
    if func.__closure__:
        original_closure_vals = [func.__closure__[i].cell_contents for i in range(len(func.__closure__))]

    @wraps(func)
    def wrapper(*args, **kwargs):
        input_kwargs = {}
        for k, v in kwargs.items():
            if k in original_arg_names:
                input_kwargs[k] = v
            elif k in func.__code__.co_freevars:
                func.__closure__[func.__code__.free_vars.index(k)].cell_contents = v
            elif k in gl:
                gl[k] = v
            else:
                raise AttributeError(f'Unexpected attribute {k} for {func.__name__}')

        result = new_func(*args, **input_kwargs)
        if original_closure_vals:
            for i in range(len(original_closure_vals)):
                func.__closure__[i].cell_contents = original_closure_vals[i]
        gl.clear()
        gl.update(original_globals)
        return result

    return wrapper
