import builtins
import sys
from collections import ChainMap


class new_scope:

    def __enter__(self):
        self.stack_frame = sys._getframe(0).f_back
        variables = ChainMap(
            self.stack_frame.f_locals,
            self.stack_frame.f_globals,
            builtins.__dict__
        )
        self.this = This(variables)
        return self.this

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.stack_frame.f_locals["this"]
        self.this.clear()
        del self.this


class This:

    def __init__(self, scope_variables: ChainMap):
        self.__dict__["variables"] = scope_variables.copy()
        self.__dict__["new_variables"] = dict()

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        elif item in self.new_variables:
            return self.new_variables[item]
        else:
            return self.variables[item]

    def __setattr__(self, key, value):
        self.new_variables[key] = value

    def clear(self):
        self.new_variables.clear()
