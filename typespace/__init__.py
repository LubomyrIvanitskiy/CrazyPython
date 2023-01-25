import inspect
from functools import lru_cache, wraps
from collections import defaultdict


# IN: assert_arguments
@lru_cache
def _get_signature(func):
    return inspect.signature(func)


def assert_arguments(func, *args, **kwargs):
    arguments = _get_signature(func).bind(*args, **kwargs).arguments
    for name, annotation in func.__annotations__.items():
        traverse(annotation, arguments[name])


def assert_failed(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except AssertionError:
        pass
    else:
        raise AssertionError(f"An assertion for {func} is expected to be raised")


def traverse(target, *args, **kwargs):

    if target is ...:
        return None
    if isinstance(target, type):
        assert isinstance(args[0], target), f'{target.__name__}\'s argument should be of type {target}'
        return target

    if not callable(target):
        assert target == args[0]
        return target
    else:
        assert_arguments(target, *args, **kwargs)
        return target(*args, **kwargs)


def overload(func):
    if 'overloads' not in overload.__dict__:
        overload.overloads = defaultdict(list)
    overload.overloads[func.__name__].append(func)

    def wrapper(*args, **kwargs):
        for f in overload.overloads[func.__name__]:
            try:
                assert_arguments(f, *args, **kwargs)
                return f(*args, **kwargs)
            except AssertionError:
                pass
        else:
            raise AssertionError(f"No function overload found for {func}")

    return wrapper


def typed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return traverse(func, *args, **kwargs)

    return wrapper

    # ------------------- HELPERS ---------------------


def And(*funcs):
    def wrapper(*args, **kwargs):
        tuple(traverse(fun, *args, **kwargs) for fun in funcs)

    return wrapper


def Or(*funcs):
    def wrapper(*args, **kwargs):
        for fun in funcs:
            try:
                traverse(fun, *args, **kwargs)
                break
            except AssertionError:
                pass
        else:
            raise AssertionError(f'All precomputes failed for Or({funcs})')

    return wrapper


def Xor(*funcs):
    def wrapper(*args, **kwargs):
        success_count = 0
        for fun in funcs:
            try:
                traverse(fun, *args, **kwargs)
                success_count += 1
            except AssertionError:
                pass

        assert success_count == 1, f'Only single type-function from {funcs} should success'

    return wrapper


def Not(fun):
    def wrapper(*args, **kwargs):
        assert_failed(traverse, fun, *args, **kwargs)

    return wrapper


def Collection(*margs, **mkwargs):
    def wrapper(obj):
        for aarg, marg in zip(obj, margs):
            traverse(marg, aarg)
        for m in mkwargs:
            traverse(mkwargs[m], obj[m])

    return wrapper


def Object(**members):
    def wrapper(obj):
        for m in members:
            traverse(members[m], getattr(obj, m))

    return wrapper
