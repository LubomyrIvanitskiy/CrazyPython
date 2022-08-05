# Thanks to https://stackoverflow.com/questions/27550228/can-you-patch-just-a-nested-function-with-closure-or-must-the-whole-outer-fun
import builtins
import inspect
from types import FunctionType as function

from inner_decorator import closures_hook


def replace_inner_function(outer, new_inner, name=None):
    """Replace a nested function code object used by outer with new_inner

    The replacement new_inner must use the same name and must at most use the
    same closures as the original.

    """
    if hasattr(new_inner, '__code__'):
        # support both functions and code objects
        new_closure = new_inner.__closure__
        new_inner = new_inner.__code__

    # find original code object so we can validate the closures match
    ocode = outer.__code__
    function, code = type(outer), type(ocode)
    iname = name if name else new_inner.co_name
    orig_inner = next(
        const for const in ocode.co_consts
        if isinstance(const, code) and const.co_name == iname)

    # you can ignore later closures, but since they are matched by position
    # the new sequence must match the start of the old.
    # print("outer_cellvars", outer.__code__.co_cellvars)
    # print("freevars", orig_inner.co_freevars, new_inner.co_freevars)
    # print("var_names", orig_inner.co_varnames, new_inner.co_varnames)

    assert (orig_inner.co_freevars[:len(new_inner.co_freevars)] ==
            new_inner.co_freevars), 'New closures must match originals'

    # replace the code object for the inner function
    new_consts = tuple(
        new_inner if const is orig_inner else const
        for const in outer.__code__.co_consts)

    # create a new code object with the new constants
    try:
        # Python 3.8 added code.replace(), so much more convenient!
        ncode = ocode.replace(
            co_consts=new_consts
        )
    except AttributeError:
        # older Python versions, argument counts vary so we need to check
        # for specifics.
        args = [
            ocode.co_argcount, ocode.co_nlocals, ocode.co_stacksize,
            ocode.co_flags, ocode.co_code,
            new_consts,  # replacing the constants
            ocode.co_names, ocode.co_varnames, ocode.co_filename,
            ocode.co_name, ocode.co_firstlineno, ocode.co_lnotab,
            ocode.co_freevars, ocode.co_cellvars,
        ]
        if hasattr(ocode, 'co_kwonlyargcount'):
            # Python 3+, insert after co_argcount
            args.insert(1, ocode.co_kwonlyargcount)
        # Python 3.8 adds co_posonlyargcount, but also has code.replace(), used above
        ncode = code(*args)

    # and a new function object using the updated code object
    res = function(
        ncode, outer.__globals__, outer.__name__,
        outer.__defaults__, outer.__closure__
    )
    return res


def inner_decorator(**kwargs):
    def decorator(outer_func):
        code = type(outer_func.__code__)
        inner_functions = [f for f in outer_func.__code__.co_consts[1:] if isinstance(f, code)]

        new_outer_func = outer_func
        for f in inner_functions:
            if f.co_name in kwargs:
                inner_function = function(f, globals())
                wrapped_func = kwargs[f.co_name](inner_function)

                def func_without_closure(*args, **kwargs):
                    from inner_decorator import closures_hook
                    import inspect
                    wrapped_func_ = getattr(closures_hook, inspect.stack()[0][0].f_code.co_name + inspect.stack()[0][
                        0].f_code.co_filename + str(inspect.stack()[0][0].f_code.co_firstlineno))
                    return wrapped_func_(*args, **kwargs)

                func_without_closure.__name__ = f.co_name
                func_without_closure.__code__ = func_without_closure.__code__.replace(
                    co_name=f.co_name
                )
                setattr(closures_hook,
                        f.co_name + func_without_closure.__code__.co_filename + str(
                            func_without_closure.__code__.co_firstlineno),
                        wrapped_func)
                new_outer_func = replace_inner_function(new_outer_func, func_without_closure, name=f.co_name)
        new_conames = []
        for f_name in outer_func.__code__.co_names:
            if f_name in kwargs:
                if f_name in globals():
                    f = globals()[f_name]
                elif f_name in dir(builtins):
                    f = getattr(builtins, f_name)
                else:
                    raise TypeError("Cannot find passed function", f_name)
                wrapped_f_name = "_tmpkmd45_wrapped_" + f_name
                inspect.stack()[1][0].f_globals[wrapped_f_name] = kwargs[f_name](f)
                new_conames.append(wrapped_f_name)
            else:
                new_conames.append(f_name)
        new_outer_func.__code__ = new_outer_func.__code__.replace(
            co_names=tuple(new_conames)
        )
        return new_outer_func

    return decorator
