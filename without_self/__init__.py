import inspect
from collections import ChainMap


def define_args(func, *args, **kwargs):
    try:
        spec = inspect.getfullargspec(func)

        positional_args = []
        defaults_count = 0 if not spec.defaults else len(spec.defaults)
        for i, a in enumerate(spec.args[:len(spec.args) - defaults_count]):
            if i < len(args):
                positional_args.append(args[i])
            elif a in kwargs:
                positional_args.append(kwargs[a])
            else:
                raise TypeError(f"Value for argument {a} cannot be obtained")

        named_args = dict()

        for i, a in enumerate(spec.args[len(spec.args) - defaults_count:]):
            if len(spec.args) - defaults_count + i < len(args):
                positional_args.append(args[len(spec.args) - defaults_count + i])
                if a in kwargs:
                    print(f"Warning! Conflicting declaration. You have provided {a} in the kwargs, "
                          f"but the value also can be (and will be) obtained from your positional arguments. "
                          f"Make sure this is what you expect!")
            elif a in kwargs:
                named_args[a] = kwargs[a]
            else:
                # named_args[a] = spec.defaults[i]
                positional_args.append(spec.defaults[i])  # TODO check if previous line is not better.
                # This line works for buildins functions like str.replace
        if spec.varargs:
            if len(args) > len(positional_args):
                positional_args.extend(args[len(positional_args):])

        if spec.kwonlyargs:
            kwonly_defaults_count = len(spec.kwonlydefaults)
            for i, a in enumerate(spec.kwonlyargs[:len(spec.kwonlyargs) - kwonly_defaults_count]):
                if a in kwargs:
                    named_args[a] = kwargs[a]
                else:
                    raise TypeError(f"Value for KWONLY argument {a} is not provided or is not named argument")
            for i, a in enumerate(spec.kwonlyargs[len(spec.kwonlyargs) - kwonly_defaults_count:]):
                if a in kwargs:
                    named_args[a] = kwargs[a]
                else:
                    named_args[a] = spec.kwonlydefaults[i]

        if spec.varkw:
            if len(kwargs) > len(named_args):
                named_args.update(kwargs)
    except Exception as e:
        positional_args = args
        named_args = kwargs
    return tuple(positional_args), named_args


def noself(func):
    return FunctionDescriptor(func)


class FunctionDescriptor:

    def __init__(self, original_function):
        self.original_function = original_function

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type=None):
        def wrapper(*args, **kwargs):
            kwargs = ChainMap(kwargs, {"self_" + k: v for k, v in vars(obj).items()} if obj else {})
            new_args, new_kwargs = define_args(self.original_function, *args, **kwargs)
            return self.original_function(*new_args, *new_kwargs)

        return wrapper


class LogDict(dict):

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if callable(value) and not key.startswith("__"):
            super(LogDict, self).__setitem__(key, FunctionDescriptor(value))
        else:
            super(LogDict, self).__setitem__(key, value)


class NoSelf(type):

    @classmethod
    def __prepare__(metacls, name, bases):
        return LogDict()
