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


# Test the function
original_dict = {"a": 1, "b": {"c": 2, "d": [{"e": 3}, 4]}, "f": [5, 6]}
copied_dict = deep_copy_dict(original_dict)

print(copied_dict)


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


def trace_on(home=os.getcwd(), include_privates=False, include_builtins=False, include_libs=False):
    def trace_lines(frame, event, arg):
        if 'scopes' not in trace_lines.__dict__:
            trace_lines.scopes = [{}]
        if 'prev_line' not in trace_lines.__dict__:
            trace_lines.prev_line = '', 0, 0, ''
        co = frame.f_code
        file_name = co.co_filename
        if not include_libs:
            if not file_name.startswith(home) or ('<' in file_name) or ('site-packages' in file_name):
                return trace_lines

        func_name = co.co_name
        line_no = frame.f_lineno
        line = linecache.getline(file_name, line_no).strip('\n')

        if event == 'call':
            trace_lines.reserv_prev_line = trace_lines.prev_line
            print(f'\n\033[1m{trace_lines.prev_line[0]}() --> {func_name}()\033[0m: File "{os.path.relpath(file_name)}", line {line_no}')
            trace_lines.prev_line = func_name, trace_lines.prev_line[2], line_no, line
            trace_lines.scopes.append({})
            return trace_lines
        locs = ((k, v) for k, v in deep_copy_dict(frame.f_locals).items())
        if not include_privates:
            locs = ((k, v) for k, v in locs if not k.startswith('_'))
        if not include_builtins:
            locs = ((k, v) for k, v in locs if not hasattr(v, '__module__') or not v.__module__.startswith('builtins'))
        locs = dict(locs)
        diff = dict_diff(trace_lines.scopes[-1], locs)
        # if diff:
        prev_func_name, pprev_line_no, prev_line_no, prev_line = trace_lines.prev_line
        code_text_lines = textwrap.wrap(prev_line, width=CODE_WIDTH)
        vars_lines = textwrap.wrap(str(diff), width=VARS_WIDTH)
        lines = []
        numbers = [prev_line_no]
        for n, c, v in zip_longest(numbers, code_text_lines, vars_lines, fillvalue=' '):
            color_c = highlight(c, PythonLexer(), TerminalFormatter(bg='dark')).rstrip() if c != ' ' else ' '
            color_vars = highlight(v, PythonLexer(), TerminalFormatter(bg='dark')).rstrip() if v != ' ' else ' '
            lines.append(f'{n:<6} {color_c:<{CODE_WIDTH - len(c) + len(color_c)}} # {color_vars:<{VARS_WIDTH-len(v)+len(color_vars)}}')

        if prev_line_no - pprev_line_no > 1:
            print(f'{pprev_line_no + 1}-{prev_line_no} ...')
        print('\n'.join(lines))
        trace_lines.prev_line = func_name, prev_line_no, line_no, line  # f'{tab}{line_no}\t\t{line}'
        trace_lines.scopes[-1] = locs

        if event == 'return':
            trace_lines.prev_line = trace_lines.reserv_prev_line
            trace_lines.scopes.pop()
            print(f'\033[1m{trace_lines.prev_line[0]}() <-- {func_name}()\n\n[CONTINUE] {trace_lines.prev_line[0]}()\033[0m:')

        return trace_lines

    sys.settrace(trace_lines)


def trace_off():
    sys.settrace(orig_trace)
