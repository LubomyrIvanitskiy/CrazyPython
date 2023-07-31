import copy
import linecache
import os
import sys

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

def trace_on(home=os.getcwd(), include_privates=False, include_builtins=False, include_libs=False):
    def trace_lines(frame, event, arg):
        if 'scopes' not in trace_lines.__dict__:
            trace_lines.scopes = [{}]
        if 'prev_line' not in trace_lines.__dict__:
            trace_lines.prev_line = ''
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
            tab = '\t'*len(trace_lines.scopes)
            trace_lines.prev_line = f'{tab}{line_no}\t\t{line}'
            print(f'{tab}FUNCTION {func_name} ({os.path.relpath(file_name)}:{line_no})')
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
        tab = '\t'*len(trace_lines.scopes)
        print(f'{trace_lines.prev_line}\t\t# {diff}')
        trace_lines.prev_line = f'{tab}{line_no}\t\t{line}'
        trace_lines.scopes[-1] = locs

        if event == 'return':
            trace_lines.prev_line = trace_lines.reserv_prev_line
            trace_lines.scopes.pop()
        return trace_lines

    sys.settrace(trace_lines)


def trace_off():
    sys.settrace(orig_trace)
