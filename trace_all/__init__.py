from collections import defaultdict, ChainMap
from itertools import zip_longest
import linecache
import os
import sys

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

import textwrap

orig_trace = sys.gettrace()

import tokenize
import io


def extract_nested_objects(code_str):
    g = tokenize.tokenize(io.BytesIO(code_str.encode('utf-8')).readline)

    nested_objects = []
    current_object = ""

    for tok in g:
        if tok.type == tokenize.NAME:
            if current_object:
                if current_object.endswith('[') or current_object.endswith('.'):
                    current_object += tok.string
                else:
                    nested_objects.append(current_object)
                    current_object = tok.string
            else:
                current_object = tok.string

        elif tok.type == tokenize.OP:
            if tok.string == '.':
                if current_object:
                    current_object += tok.string

            elif tok.string == '[':  # array index access begins
                current_object += tok.string

            elif tok.string == ']':  # array index access ends
                current_object += tok.string

            elif tok.string == ',':  # argument separator
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""
            elif tok.string == '(':  # end of function call or grouping
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""

            elif tok.string == ')':  # end of function call or grouping
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""

        elif tok.type == tokenize.NUMBER or tok.type == tokenize.STRING:
            if current_object.endswith('['):  # inside array index access
                current_object += tok.string

    if current_object:
        nested_objects.append(current_object)

    return [ex for ex in nested_objects if '.' in ex or '[' in ex]


def get_variables(code_line, line_no, frame_locals, frame_globals, frame_names, with_expressions=True):
    # print("GET_TOKENS", code_line)
    expressions = []
    if 'previous' not in get_variables.__dict__:
        get_variables.previous = None
    try:
        if get_variables.previous and get_variables.previous[0] == line_no - 1:
            code_line = f'{get_variables.previous[1]}\n{code_line}'
            print('MULTILINES', code_line)
        else:
            get_variables.previous = None
        tokens = tokenize.tokenize(io.BytesIO(code_line.encode('utf-8')).readline)
        names = {token.string for token in tokens if token.type == tokenize.NAME}
        if with_expressions:
            expressions = extract_nested_objects(code_line)

    except tokenize.TokenError as e:
        if get_variables.previous and get_variables.previous[0] == line_no - 1:
            code_line = f'{get_variables.previous[1]}\n{code_line}'
        get_variables.previous = (line_no, code_line)
        return {}, []
    locs_ = frame_locals
    glob_chain = frame_globals  # ChainMap(frame_globals, __builtins__)
    globs_ = {k: glob_chain[k] for k in frame_names if k in glob_chain}
    context = ChainMap(locs_, globs_)
    if with_expressions:
        return {n: context[n] for n in names if n in context}, expressions
    else:
        return {n: context[n] for n in names if n in context}


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
        var_mode='used',  # diff, used, used+, all, none
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
            locs = ((k, v) for k, v in locs if
                    not hasattr(v, '__module__') or (v.__module__ and not v.__module__.startswith('builtins')))
        locs = dict(locs)
        var_dict = None
        if var_mode == 'diff':
            var_dict = dict_diff(trace_lines.scopes[-1], locs)
        elif var_mode == 'all':
            var_dict = locs
        elif var_mode.startswith('used'):
            with_expressions = var_mode.endswith('+')
            if with_expressions:
                var_dict, expressions = get_variables(trace_lines.prev_line[-1], trace_lines.prev_line[-2], locs,
                                                      frame.f_globals, co.co_names, with_expressions=True)

                if expressions:
                    for exp in expressions:
                        if exp not in var_dict:
                            try:
                                var_dict[exp] = eval(exp, frame.f_globals, frame.f_locals)
                            except:
                                pass

            else:
                var_dict = get_variables(trace_lines.prev_line[-1], trace_lines.prev_line[-2], locs,
                                                      frame.f_globals, co.co_names)
        elif var_mode == 'none':
            var_dict = {}
        _show_line(trace_lines.prev_line, var_dict, background, code_width=code_size, vars_width=vars_size)
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
                 var_mode='used',  # diff, used, all, none
                 background: str = 'dark',
                 code_size: int = CODE_WIDTH,
                 vars_size: int = VARS_WIDTH
                 ):
        self.home = home
        self.include_privates = include_privates
        self.include_builtins = include_builtins
        self.include_libs = include_libs
        self.targets = targets
        self.var_mode = var_mode
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
            var_mode=self.var_mode,
            background=self.background,
            code_size=self.code_size,
            vars_size=self.vars_size
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        trace_off()
