import os
import runpy
import sys
import pathlib

from importlib.machinery import PathFinder

launcher_path = sys.argv[1]
if not launcher_path.endswith(".py"):
    launcher_module_path = launcher_path
    launcher_path = "." + os.sep + launcher_path.replace(".", os.sep) + ".py"
else:
    launcher_module_path = launcher_path[-2:].replace(os.sep, ".")

########## Try to find the root
cwd_parts = pathlib.Path(os.getcwd()).parts
launcher_parts = pathlib.Path(launcher_path).parts
root_path = None
for i in range(len(cwd_parts)):
    try_path = os.sep.join(cwd_parts[:len(cwd_parts) - i] + launcher_parts)
    if os.path.exists(try_path) and not os.path.isdir(try_path):
        root_path = os.sep.join(cwd_parts[:len(cwd_parts) - i])
        break
if not root_path:
    raise ValueError("Cannot find the module specified")

sys.path.insert(0, os.path.realpath(root_path))

os.chdir(os.path.realpath(root_path))


class Loader(object):
    def __init__(self, module):
        self.module = module

    def load_module(self, fullname):
        return self.module


class Importer(PathFinder):
    def find_spec(self, fullname, path=None, target=None):
        spec = super().find_spec(fullname, path, target)
        found_paths = []
        for entry in sys.path:
            if len(entry) > 0 and spec.origin.startswith(entry):
                found_paths.append(entry)
        sorted_found_path = sorted(found_paths, key=lambda item: len(item))
        new_module_name = spec.origin[len(sorted_found_path[0]) + 1:-3].replace("\\", ".")
        if new_module_name.endswith("__init__"):
            new_module_name = new_module_name[:-len(".__init__")]
        return super().find_spec(new_module_name, path, target)


sys.meta_path.insert(0, Importer())

reserved_argv = sys.argv.copy()
sys.argv.clear()
sys.argv.extend([launcher_module_path] + (reserved_argv[2:] if len(reserved_argv) > 2 else []))

runpy.run_module(launcher_module_path, {}, "__main__")
