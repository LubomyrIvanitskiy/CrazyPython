import inspect
from functools import lru_cache, wraps
from collections import defaultdict

ENABLED = False


# IN: assert_arguments
@lru_cache
def _get_signature(func):
    return inspect.signature(func)


def assert_arguments(func, *args, **kwargs):
    arguments = _get_signature(func).bind(*args, **kwargs).arguments
    for name, annotation in func.__annotations__.items():
        if name != 'return':
            result = traverse(annotation, arguments[name], __param_name=name)
            assert result is not False, f"Result for {func.__name__} is {result}"


def assert_output(func, output):
    if 'return' in func.__annotations__:
        traverse(func.__annotations__['return'], output, __param_name='return')


def assert_failed(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        assert result is False
    except AssertionError:
        pass
    else:
        raise AssertionError(f"An assertion for {func} is expected to be raised")


def traverse(target, *args, __param_name=None, **kwargs):
    if target is ...:
        return None
    if isinstance(target, type):
        assert isinstance(args[0],
                          target), f'{__param_name if __param_name is not None else args[0].__class__.__name__}\'s should be of type {target}'
        return target

    if not callable(target):
        assert target == args[0]
        return target
    elif hasattr(target, '__annotations__'):
        assert_arguments(target, *args, **kwargs)
        result = target(*args, **kwargs)
        assert_output(target, result)
        return result
    else:
        return target(*args, **kwargs)


def overload(func):
    if not ENABLED:
        return func
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
    if not ENABLED:
        return func

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


def Eq(fun):
    def wrapper(arg):
        assert fun == arg

    return wrapper


def Collection(*margs, **mkwargs):
    def wrapper(obj):
        for i, aarg, marg in enumerate(zip(obj, margs)):
            traverse(marg, aarg, __param_name=i)
        for m in mkwargs:
            traverse(mkwargs[m], obj[m], __param_name=m)

    return wrapper


def Object(**members):
    def wrapper(obj):
        for m in members:
            traverse(members[m], getattr(obj, m), __param_name=m)

    return wrapper


def configure(
        enabled: bool = ENABLED
):
    global ENABLED
    ENABLED = enabled
