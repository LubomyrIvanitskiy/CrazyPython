from __future__ import annotations
import builtins
import inspect
from inspect import isclass
from typing import Dict, List
from collections import namedtuple
from functools import wraps

Restriction = namedtuple("Restriction", "condition, check")


def convert_to_type(object_name):
    if object_name in globals() and isclass(globals()[object_name]):
        return globals()[object_name]
    elif hasattr(builtins, object_name) and isclass(getattr(builtins, object_name)):
        return getattr(builtins, object_name)
    else:
        return None


def append_to_dict(dict_, key, value):
    if key in dict_:
        dict_[key].append(value)
    else:
        dict_[key] = [value]


def restricted(func):
    argspec = inspect.getfullargspec(func)

    exec_outs = {}

    def get_exec_output_name(arg_name):
        return "res_" + arg_name

    def get_exec_output(arg_name):
        return exec_outs[get_exec_output_name(arg_name)]

    def put_exec_output(arg_name, value):
        exec_outs[get_exec_output_name(arg_name)] = value

    compilled_restictions: Dict[str, List] = {}
    for a, restriction in argspec.annotations.items():
        for command in restriction.split(","):
            command = command.strip("' []")
            type_ = convert_to_type(command)
            if type_ is not None:
                append_to_dict(compilled_restictions, a,
                               Restriction(command,
                                           lambda a_name, scope, type__=type_: put_exec_output(a_name,
                                                                                               isinstance(
                                                                                                   scope[
                                                                                                       a_name],
                                                                                                   type__))))
            else:
                compiled_command = compile(get_exec_output_name(a) + "=" + command, "something", "exec")
                append_to_dict(compilled_restictions, a, Restriction(command,
                                                                    lambda a_name, scope,
                                                                           compiled_command_=compiled_command: exec(
                                                                        compiled_command_, scope,
                                                                        exec_outs)))

    function_globals = globals()

    @wraps(func)
    def wrapper(*args, **kwargs):
        all_values = list(args) + list(kwargs.values())
        scope = dict(zip(argspec.args, all_values))
        scope.update(function_globals)
        for a, v in zip(argspec.args, all_values):
            if a not in compilled_restictions:
                continue
            for restriction in compilled_restictions[a]:
                restriction.check(a, scope)
                assert get_exec_output(a), f"{restriction.condition} is False"
        return func(*args, **kwargs)

    return wrapper