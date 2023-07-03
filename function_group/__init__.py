import builtins
import sys
from collections import ChainMap
from copy import  copy

def tmp_foo():
    pass

FuncType = type(tmp_foo)
class _Context:

    def get_name(self):
        if self._name is None:
            locals = self._get_locals()
            self._name = next(k for k in locals if isinstance(locals[k], _Context))

        return self._name

    def _get_frame_dict(self):
        return ChainMap(
            self.stack_frame.f_locals,
            self.stack_frame.f_globals
        )

    def _get_locals(self):
        if self._locals is not None:
            return self._locals
        exit_dict = self._get_frame_dict()
        return {k: exit_dict[k] for k in set(exit_dict.keys()) - self.enter_vars}

    def __init__(self, stack_frame):
        self.stack_frame = stack_frame
        self.enter_vars = set(self._get_frame_dict())
        self._name = None
        self._locals = None

    def on_exit(self):
        self._locals = self._get_locals()
        self._clear()
        for l in self._locals:
            if isinstance(self._locals[l], FuncType):
                self._locals[l].__globals__.update(self._locals)

    def __getattr__(self, item):
        if item in self._locals:
            return self._locals[item]
        raise AttributeError(f"No attribute {item}")

    def _clear(self):
        exit_dict = self._get_frame_dict()
        for v in self._locals:
            if isinstance(exit_dict[v], _Context):
                continue
            del self.stack_frame.f_locals[v]

    def __str__(self):
        print("str")
        return f"<{self.get_name()}-context>"


class _Functions:

    def __enter__(self):
        self.context = _Context(sys._getframe(0).f_back)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.on_exit()
        print("EXIT", self.context._locals)


functions = _Functions()
