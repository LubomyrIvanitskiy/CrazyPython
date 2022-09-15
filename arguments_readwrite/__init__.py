import inspect
from collections import ChainMap
from functools import wraps, cache
from typing import TypeVar

T = TypeVar('T')


class ControlAccess:
    _code: int

    @classmethod
    def is_readable(cls):
        return cls._code & 1 > 0

    @classmethod
    def is_writable(cls):
        return (cls._code >> 1) & 1 > 0

    @classmethod
    def is_executable(cls):
        return (cls._code >> 2) & 1 > 0


class AccessType:

    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    @cache
    def __getitem__(self, item: T) -> T:
        type_name = item.__name__ if isinstance(item, type) else str(item)
        class_ = type(self.name.capitalize() + type_name.capitalize(), (ControlAccess,), {})
        class_._code = self.code
        return class_


code_to_access_type = dict()
BlackBox = AccessType("Read", 0b000)
code_to_access_type[BlackBox.code] = BlackBox
Read = AccessType("Read", 0b001)
code_to_access_type[Read.code] = Read
Write = AccessType("Write", 0b010)
code_to_access_type[Write.code] = Write
Exec = AccessType("Exec", 0b100)
code_to_access_type[Exec.code] = Exec
ReadWrite = AccessType("ReadWrite", 0b011)
code_to_access_type[ReadWrite.code] = ReadWrite
ReadExec = AccessType("ReadExec", 0b101)
code_to_access_type[ReadExec.code] = ReadExec
WriteExec = AccessType("WriteExec", 0b110)
code_to_access_type[WriteExec.code] = WriteExec
ReadWriteExec = AccessType("ReadWriteExec", 0b111)
code_to_access_type[ReadWriteExec.code] = ReadWriteExec


class SetAttrDescriptor:

    def __init__(self, original_function):
        self.original_function = original_function

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type=None):
        def no_setattr(*args, **kwargs):
            raise RuntimeError("Cannot modify read-only function argument")

        if "__control_access__" in vars(obj):
            if not obj.__control_access__.is_writable():
                return no_setattr
        return self.original_function.__get__(obj)


class GetAttrDescriptor:

    def __init__(self, original_function):
        self.original_getter = original_function

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type=None):
        def no_getattr(_):
            raise RuntimeError("Cannot read from non-readable function argument")

        def wrap_result(name):
            result = self.original_getter.__get__(obj)(name)
            if not name.startswith("__") and "__control_access__" in self.original_getter(obj, "__dict__"):
                result = _make_controlled_object(result, self.original_getter(obj, "__control_access__"))
            return result

        if "__control_access__" in self.original_getter(obj, "__dict__"):
            if not self.original_getter(obj, "__dict__")["__control_access__"].is_readable():
                return no_getattr
        return wrap_result


class CallDescriptor:

    def __init__(self, original_function):
        self.original_function = original_function

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type=None):
        def no_call(*args, **kwargs):
            raise RuntimeError("Cannot call the the method of non-executable objects")

        if "__control_access__" in vars(obj):
            if not obj.__control_access__.is_executable():
                return no_call
        return self.original_function.__get__(obj)


def _make_controlled_object(obj, control_access_):
    if not isinstance(obj, type):
        if "__dict__" in dir(obj):
            obj.__control_access__ = control_access_
            try:
                type(obj).__setattr__ = SetAttrDescriptor(type(obj).__setattr__)
                type(obj).__getattribute__ = GetAttrDescriptor(type(obj).__getattribute__)
            except Exception as e:
                pass
        if callable(obj):
            original_obj = obj

            def wrapper(*args, **kwargs):
                if control_access_.is_executable() or control_access_.is_readable() and obtain_access_control(
                        original_obj).code == 0b001:  # means we may garantee that no the function is read only
                    original_obj(*args, **kwargs)
                else:
                    raise RuntimeError("Cannot call non-executable objects")

            obj = wrapper
    return obj


def control_access(func):
    sign = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bargs = sign.bind(*args, **kwargs)
        new_args = list()
        new_kwargs = dict()
        for arg in bargs.arguments:
            arg_value = bargs.arguments[arg]
            arg_declared_type = sign.parameters[arg].annotation
            if ControlAccess in arg_declared_type.__bases__:
                arg_value = _make_controlled_object(arg_value, arg_declared_type)
            if arg not in kwargs:
                new_args.append(arg_value)
            else:
                new_kwargs[arg] = arg_value
        return func(*new_args, **new_kwargs)

    wrapper.__control_access__ = True
    sig = inspect.signature(func)
    sig = sig.replace(parameters=tuple(sig.parameters.values())[:])
    wrapper.__signature__ = sig

    return wrapper


def obtain_access_control(func):
    sign = inspect.signature(func) if not inspect.ismethod(func) else inspect.signature(func.__func__)
    mask = 0b000
    for p in sign.parameters:
        if ControlAccess in sign.parameters[p].annotation.__bases__:
            mask |= sign.parameters[p].annotation._code
        else:
            return ReadWriteExec
    return code_to_access_type[mask]


class AccessGuard(type):
    """
    Ensures all subclasses inherit @access_control annotation and argument types
    """

    def __new__(cls, *args, **kwargs):
        name, bases, namespace = args
        for m in namespace:
            for b in bases:
                if m in dir(b):
                    base_member = getattr(b, m)
                    if "__control_access__" in dir(base_member):
                        base_arg_spec = inspect.getfullargspec(base_member)
                        arg_spec = inspect.getfullargspec(namespace[m])
                        new_arg_annotations = dict()  # let's try to inherit type hints from the base class
                        for p in inspect.signature(namespace[m]).parameters:
                            if p not in arg_spec.annotations and p in base_arg_spec.annotations:
                                new_arg_annotations[p] = base_arg_spec.annotations[p]
                            elif p in arg_spec.annotations:
                                new_arg_annotations[p] = arg_spec.annotations[p]

                        if new_arg_annotations != base_arg_spec.annotations:
                            raise AttributeError(
                                f"Signature (with type hints) of overridden methods with control_access "
                                f"should match the signature of base method.\nSignature of {m} should be {inspect.signature(base_member)} ")
                        sig = inspect.signature(namespace[m])
                        new_params = []
                        for p in sig.parameters.values():
                            new_params.append(inspect.Parameter(p.name, p.kind, default=p.default,
                                                                annotation=new_arg_annotations[
                                                                    p.name] if p.name in new_arg_annotations else ReadWriteExec[object]))
                        sig = sig.replace(parameters=tuple(new_params)[:])
                        namespace[m].__signature__ = sig
                        namespace[m] = control_access(namespace[m])
                        break

        return super().__new__(cls, *args, **kwargs)
