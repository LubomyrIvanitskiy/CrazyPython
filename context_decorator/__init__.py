import sys
import inspect


class decorator:

    def __init__(self, decorator):
        self.decorator = decorator

    def __enter__(self):
        self.enter_locals = dict(**sys._getframe(0).f_back.f_locals)

    def __exit__(self, exc_type, exc_val, exc_tb):
        exit_locals = sys._getframe(0).f_back.f_locals
        new_funcs = set(f for f in exit_locals if f not in self.enter_locals if inspect.isfunction(exit_locals[f]))
        exit_locals.update({
            f_name: self.decorator(exit_locals[f_name]) for f_name in new_funcs
        })

