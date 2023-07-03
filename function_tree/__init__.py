import inspect
from types import FunctionType


class accessed_by:

    def __init__(self, *funcs):
        self.funcs = tuple(f.__name__ if isinstance(f, FunctionType) else f for f in funcs)
        caller_globals = None
        for f in inspect.stack():
            if 'with accessed_by' in f.code_context[0]:
                caller_globals = f[0].f_globals
                break
        if caller_globals is None:
            raise RuntimeError()
        self.caller_globals = caller_globals

    def __enter__(self):
        self.pre_scope_globals = self.caller_globals.copy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        wrapped_funcs = dict()
        for f_name in self.funcs:
            func = self.caller_globals[f_name]
            # def wrapper(*args, __my_fun=f_name, **kwargs):
            #     return
            func = FunctionType(
                func.__code__,
                self.caller_globals.copy(),
                name=func.__name__,
                argdefs=inspect.getfullargspec(func).defaults,
                closure=func.__closure__
            )
            wrapped_funcs[f_name] = func

        # for new_var in set(self.caller_globals) - set(self.pre_scope_globals):
        #     variable = self.caller_globals[new_var]
        #     if isinstance(variable, FunctionType):
        #         variable.__dict__['__accessors__'] = self.funcs
        self.caller_globals.clear()
        self.caller_globals.update(self.pre_scope_globals)
        self.caller_globals.update(wrapped_funcs)
        return False
