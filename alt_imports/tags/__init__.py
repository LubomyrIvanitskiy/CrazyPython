import os.path
import sys
import types
from . import _build_module

from py._builtin import execfile


def tag(*names):
    def decor(func):
        for name in names:
            name = "tags." + name
            name_parts = name.split(".")
            for i in range(len(name_parts)):
                prefix = ".".join(name_parts[:i + 1])
                if prefix not in sys.modules:
                    sys.modules[prefix] = types.ModuleType(prefix)
            setattr(sys.modules[name], func.__name__, func)
        return func

    return decor


manifest_file = "examples/__manifest__.py"
if os.path.exists(manifest_file):
    execfile(manifest_file)

_build_module.materialize_tags()
