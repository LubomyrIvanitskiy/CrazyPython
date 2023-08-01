from collections import defaultdict
from itertools import zip_longest
import linecache
import os
import sys

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

import textwrap

orig_trace = sys.gettrace()


def deep_copy_dict(d):
    copy_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            copy_dict[k] = deep_copy_dict(v)
        elif isinstance(v, list):
            copy_dict[k] = [deep_copy_dict(i) if isinstance(i, dict) else i for i in v]
        else:
            copy_dict[k] = v
    return copy_dict


def dict_diff(d1, d2, diff_dict=None):
    if diff_dict is None:
        diff_dict = {}

    for k, v in d1.items():
        if k not in d2:
            diff_dict[f"-{k}"] = v
        elif v != d2[k]:
            if isinstance(v, dict) and isinstance(d2[k], dict):
                diff_dict[f"@{k}"] = dict_diff(v, d2[k], {})
            else:
                diff_dict[f"@{k}"] = f"{v} -> {d2[k]}"
    for k, v in d2.items():
        if k not in d1:
            diff_dict[f"+{k}"] = v

    return diff_dict


CODE_WIDTH = 80
VARS_WIDTH = 200

BOUND = '-' * CODE_WIDTH


def check_target(targets, file_name, func_name, line_no, variables):
    if not targets:
        return True
    found = False
    for t in targets:
        t = defaultdict(lambda: None, t.__dict__)
        tfile, tfun, tline_from, tline_to, tcond = t['file'], t['fun'], t['line_from'], t['line_to'], t['cond']
        if tfile:
            if tfile != os.path.relpath(file_name):
                continue
        if tfun:
            if tfun != func_name:
                continue
        if tline_from:
            if tline_from > line_no:
                continue
        if tline_to:
            if tline_to <= line_no and tline_to != -1:
                continue
        if tcond:
            try:
                res = eval(tcond, variables)
            except:
                res = None
            if not res:
                continue
        found = True
        break
    return found


def _show_line(prev_line, diff, background, code_width, vars_width):
    prev_func_name, pprev_line_no, prev_line_no, prev_line = prev_line
    code_text_lines = textwrap.wrap(prev_line, width=code_width)
    vars_lines = textwrap.wrap(str(diff), width=vars_width)
    lines = []
    numbers = [prev_line_no]
    for n, c, v in zip_longest(numbers, code_text_lines, vars_lines, fillvalue=' '):
        color_c = highlight(c, PythonLexer(), TerminalFormatter(bg=background)).rstrip() if c != ' ' else ' '
        color_vars = highlight(v, PythonLexer(), TerminalFormatter(bg=background)).rstrip() if v != ' ' else ' '
        lines.append(
            f'{n:<6} {color_c:<{CODE_WIDTH - len(c) + len(color_c)}} # {color_vars:<{VARS_WIDTH - len(v) + len(color_vars)}}')

    if prev_line_no - pprev_line_no > 1:
        print(f'>> {pprev_line_no + 1}-{prev_line_no} ...')
    print('>> ', '\n.. '.join(lines))


def trace_on(
        home=os.getcwd(),
        include_privates=False,
        include_builtins=False,
        include_libs=False,
        targets=None,
        background: str = 'dark',
        code_size: int = CODE_WIDTH,
        vars_size: int = VARS_WIDTH):
    bound = '-' * code_size

    def trace_lines(frame, event, arg):
        co = frame.f_code
        file_name = co.co_filename
        line_no = frame.f_lineno
        func_name = co.co_name
        line = linecache.getline(file_name, line_no).strip('\n')

        if not include_libs:
            if not file_name.startswith(home) or ('<' in file_name) or ('site-packages' in file_name):
                return trace_lines

        is_target = check_target(targets, file_name, co.co_name, line_no, frame.f_locals)

        if 'scopes' not in trace_lines.__dict__:
            trace_lines.scopes = [{}]
            if is_target:
                print(f'\n>> Start Tracing File "{os.path.relpath(file_name)}", line {line_no}')
        if 'prev_line' not in trace_lines.__dict__:
            trace_lines.prev_line = '', 0, 0, ''
        if 'path' not in trace_lines.__dict__:
            trace_lines.path = [f'{os.path.relpath(file_name)}:{func_name}']

        if event == 'call':
            trace_lines.reserv_prev_line = trace_lines.prev_line
            if is_target:
                _show_line(trace_lines.prev_line, {}, background, code_width=code_size, vars_width=vars_size)
                path = [*trace_lines.path, f'{os.path.relpath(file_name)}:{func_name}']
                path[-1] = f'\033[1m{path[-1]}\033[0m'
                path = ' ->\n##\t'.join(path)
                print(
                    f'{bound}\n## CALLSTACK:\n##\t{path}() File "{os.path.relpath(file_name)}", line {line_no}\n')
            trace_lines.prev_line = func_name, trace_lines.prev_line[2], line_no, line
            trace_lines.scopes.append({})
            trace_lines.path.append(f'{os.path.relpath(file_name)}:{func_name}')
            return trace_lines

        if not is_target:
            return trace_lines

        locs = ((k, v) for k, v in deep_copy_dict(frame.f_locals).items())
        if not include_privates:
            locs = ((k, v) for k, v in locs if not k.startswith('_'))
        if not include_builtins:
            locs = ((k, v) for k, v in locs if not hasattr(v, '__module__') or (v.__module__ and not v.__module__.startswith('builtins')))
        locs = dict(locs)
        diff = dict_diff(trace_lines.scopes[-1], locs)
        _show_line(trace_lines.prev_line, diff, background, code_width=code_size, vars_width=vars_size)
        trace_lines.prev_line = func_name, trace_lines.prev_line[2], line_no, line  # f'{tab}{line_no}\t\t{line}'
        trace_lines.scopes[-1] = locs

        if event == 'return':
            trace_lines.prev_line = trace_lines.reserv_prev_line
            trace_lines.scopes.pop()
            trace_lines.path.pop()
            print(
                f'>> \033[1m{trace_lines.prev_line[0]}() <-- {func_name}()\n>>{bound} \n>> [CONTINUE] {trace_lines.prev_line[0]}()\033[0m:')

        return trace_lines

    sys.settrace(trace_lines)


def trace_off():
    sys.settrace(orig_trace)


class tracing:

    def __init__(self,
                 home=os.getcwd(),
                 include_privates=False,
                 include_builtins=False,
                 include_libs=False,
                 targets=None,
                 background: str = 'dark',
                 code_size: int = CODE_WIDTH,
                 vars_size: int = VARS_WIDTH
                 ):
        self.home = home
        self.include_privates = include_privates
        self.include_builtins = include_builtins
        self.include_libs = include_libs
        self.targets = targets
        self.background = background
        self.code_size = code_size
        self.vars_size = vars_size

    def __enter__(self):
        trace_on(
            home=self.home,
            include_privates=self.include_privates,
            include_builtins=self.include_builtins,
            include_libs=self.include_libs,
            targets=self.targets,
            background=self.background,
            code_size=self.code_size,
            vars_size=self.vars_size
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        trace_off()
