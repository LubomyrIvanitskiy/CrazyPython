import json
import os
from collections import namedtuple
from types import SimpleNamespace

from script_args.script_args import entrypoint, launch
from trace_all import tracing
import runpy


def _parse_targets(targets):
    """
    List of targets is a list of strings in the following format:
    file_name.function_name[line_from:line_to](condition)
    :param targets:
    :return:
    """
    if targets is None:
        return None
    result = []
    for t in targets:
        t = t.strip()
        file, fun, start, end, cond = None, None, None, None, None
        if '(' in t:
            t, cond = t.split('(')
            cond = cond[:-1]
        if '[' in t:
            t, interval = t.rsplit('[', 1)
            if ':' in interval:
                start, end = interval[:-1].split(':')
                start, end = int(start), int(end)
            else:
                start, end = int(interval), int(interval) + 1
        if ':' in t:
            file, fun = t.rsplit(':', 1)
        else:
            file = t

        if file is None:
            file = ''
        if fun is None:
            fun = ''
        if start is None:
            start = 0
        if end is None:
            end = -1
        if cond is None:
            cond = ''
        result.append(SimpleNamespace(file=file, fun=fun, line_from=start, line_to=end, cond=cond))
    return result


@entrypoint(
    background='-bg',
    include_privates='-ip',
    include_builtins='-ib',
    include_libs='-il',
    targets='-t',
    code_size='-cs',
    vars_size='-vs',
)
def main(module: str, home: str = os.getcwd(),
         include_privates: bool = False,
         include_builtins: bool = False,
         include_libs: bool = False,
         targets: tuple[str] = None,
         background: str = 'dark',
         code_size: int = 80,
         vars_size: int = 200):
    targets = _parse_targets(targets)
    with tracing(
            home=home,
            include_privates=include_privates,
            include_builtins=include_builtins,
            include_libs=include_libs,
            targets=targets,
            background=background,
            code_size=code_size,
            vars_size=vars_size
    ):
        runpy.run_module(module, run_name='__main__')


if __name__ == '__main__':
    launch(globals())
