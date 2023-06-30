import sys

def entrypoint(func):
    func.is_launcher = True
    return func


def launch():
    sys_args = sys.argv[1:]
    args = []
    kwargs = {}
    potential_command = sys_args[0]
    command_function = globals()['main'] if 'main' in globals() else lambda *args, **kwargs: None
    for f_name, f in globals().items():
        if 'is_launcher' in dir(f):
            if f_name == potential_command:
                command_function = f
                sys_args = sys_args[1:]
                break

    for arg in sys_args:
        if arg.startswith('--'):
            key, _, value = arg[2:].partition('=')
            kwargs[key] = value
        elif arg.startswith('-'):
            key = arg[1:]
            kwargs[key] = True
        else:
            args.append(arg)
    return command_function(*args, **kwargs)