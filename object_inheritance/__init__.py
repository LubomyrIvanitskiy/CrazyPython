import functools
from collections import ChainMap


def set(instance, attr, value):
    """
    helper for setting a value for the instance to avoid calling __setattr__ which is customized
    """
    instance.__dict__[attr] = value


def get(instance, attr):
    """
    helper for getting a value from the instance without triggering customized __getattr__
    """
    return instance.__dict__[attr]


class MergedMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        result = super().__prepare__(name, bases)
        return result


def is_bound_method(func):
    return callable(func) and "__self__" in dir(func) and func.__self__


class Extended(metaclass=MergedMeta):
    def __init__(self, *objects):
        obj_properties = [{key: getattr(o, key) for key in dir(o)} for o in objects[::-1]]
        set(self, "map", ChainMap(*obj_properties))

    def __getattr__(self, item):
        value = get(self, "map")[item]
        if is_bound_method(value):
            value = functools.partial(value.__func__, self)
        return value

    def __setattr__(self, key, value):
        get(self, "map")[key] = value


def extend(*objects):
    return Extended(*objects)
