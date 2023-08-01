import sys
from typing import get_origin, get_args


def entrypoint(function=None, **name_aliases):
    def wrapper(func):
        func.is_entrypoint = True
        func.name_aliases = {v: k for k, v in name_aliases.items()}
        return func

    if function is not None:
        return wrapper(function)
    else:
        return wrapper


def launch(global_vars):
    sys_args = sys.argv[1:]
    args = []
    kwargs = {}
    potential_command = sys_args[0]
    command_function = global_vars['main'] if 'main' in global_vars else lambda *args, **kwargs: None
    for f_name, f in global_vars.items():
        if 'is_entrypoint' in dir(f):
            if f_name == potential_command:
                command_function = f
                sys_args = sys_args[1:]
                break

    i = 0
    while i < len(sys_args):
        if sys_args[i].startswith('-'):
            if sys_args[i] in command_function.name_aliases:
                key = command_function.name_aliases[sys_args[i]]
            else:
                key = sys_args[i]
            key = key.strip('-').replace('-', '_').lower()
            if key in command_function.__annotations__:
                argtype = command_function.__annotations__[key]
                if issubclass(argtype, bool):
                    kwargs[key] = True
                elif issubclass(argtype, int):
                    kwargs[key] = int(sys_args[i + 1])
                    i += 1
                elif issubclass(argtype, float):
                    kwargs[key] = float(sys_args[i + 1])
                    i += 1
                elif issubclass(argtype, str):
                    kwargs[key] = sys_args[i + 1]
                    i += 1
                elif issubclass(get_origin(argtype), list) or issubclass(get_origin(argtype), tuple):
                    item_type = get_args(argtype)[0]
                    value = []
                    while i + 1 < len(sys_args) and not sys_args[i + 1].startswith('-'):
                        value.append(item_type(sys_args[i + 1]))
                        i += 1
                    if key in kwargs:
                        kwargs[key] += value
                    else:
                        kwargs[key] = value
                else:
                    raise NotImplementedError
            i += 1
        else:
            args.append(sys_args[i])
            i += 1
    return command_function(*args, **kwargs)
