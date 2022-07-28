from typing import Iterable


def multiline(multiline_lambda):
    return lambda *args: multiline_lambda(*args)[-1]


def If(Condition, Then, Else):
    if Condition:
        return c if (c := Then()) is not None else ()
    else:
        return c if (c := Else()) is not None else ()


def For(generator):
    def execution(user_func):
        for item in generator:
            if isinstance(item, Iterable):
                result = user_func(*item)
                if isinstance(result, Iterable):
                    *_, result = user_func(*item)
            else:
                result = user_func(item)
                if isinstance(result, Iterable):
                    *_, result = user_func(*item)
            if is_not_empty(result):
                return result

    return execution


def is_not_empty(object):
    return (object is not None) and (object is not ...) and (object != ())
