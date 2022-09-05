import inspect
import os
import pathlib
import sys

def func_doc_string(func):
    if func.__doc__:
        return f"\"\"\"{func.__doc__}\"\"\""
    else:
        return ""


def function_stub(func):
    func_doc = func_doc_string(func)
    return f"""
def {func.__name__}{inspect.signature(func)}:
    {func_doc if func_doc else "pass"}
"""


def materialize_module(module):
    function_codes = []
    for m in vars(module):
        member = getattr(module, m)
        if inspect.isfunction(member):
            fstub = function_stub(member)
            function_codes.append(fstub)
    return "\n".join(function_codes)


def materialize_tags():
    wd = str(pathlib.Path(__file__).parent)
    if not os.path.exists(wd):
        os.mkdir(wd)
    for m in sys.modules:
        if m.startswith("tags"):
            name_parts = m.split(".")
            for i in range(len(name_parts)):
                prefix = "/".join(name_parts[:i + 1])
                path = wd+"/"+prefix[4:]
                if len(path) == 0:
                    path = ".."
                elif not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)
                if not os.path.exists(path + "/__init__.py"):
                    module_file_name = path + "/__init__.py"
                    with open(module_file_name, "w") as f:
                        f.write(materialize_module(sys.modules[m]))
