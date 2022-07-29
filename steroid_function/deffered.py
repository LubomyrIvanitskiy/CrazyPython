import inspect
import operator as ops


def arguments_merger(func1, func2):
    """
    Create merged argument declaration of composite function as well as function call body for each components
    """
    kwargs_list = []
    for func in [func1, func2]:
        spec = inspect.getfullargspec(func)
        kwargs = {arg: None for arg in spec.args}
        for i in range(len(spec.defaults) if spec.defaults else 0):
            kwargs[spec.args[-len(spec.defaults) + i]] = spec.defaults[i]
        kwargs_list.append(kwargs)

    all_args = {**kwargs_list[0], **kwargs_list[1]}

    common_args = set(kwargs_list[0]) & set(kwargs_list[1])
    for a in set(kwargs_list[0]) | set(kwargs_list[1]):
        for f, kwargs in [(func1, kwargs_list[0]), (func2, kwargs_list[1])]:
            if a in common_args:
                alias = f.__name__ + "_" + a
                all_args[alias] = kwargs[a]
                kwargs[a] = f"({alias} if {alias} else {a})"
                all_args[a] = None
            else:
                if a in kwargs:
                    kwargs[a] = a

    return kwargs_list[0], kwargs_list[1], all_args


def arg_dict_to_string(args_dictionary):
    kwargs = ", ".join([str(item[0]) + "=" + str(item[1]) for item in args_dictionary.items()])
    return f"{kwargs if kwargs else ''}"


class on_steroids:

    def __init__(self, call):
        self.call = call

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def __add__(self, other):
        return self.binary_op(other, ops.add)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.binary_op(other, ops.sub)

    def __rsub__(self, other):
        return self.binary_op(other, lambda self_, other_: ops.sub(other_, self_))

    def __mul__(self, other):
        return self.binary_op(other, ops.mul)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.binary_op(other, ops.truediv)

    def __rtruediv__(self, other):
        return self.binary_op(other, lambda self_, other_: ops.truediv(other_, self_))

    def __floordiv__(self, other):
        return self.binary_op(other, ops.floordiv)

    def __rfloordiv__(self, other):
        return self.binary_op(other, lambda self_, other_: ops.floordiv(other_, self_))

    def __pow__(self, power, modulo=None):
        return self.binary_op(power, ops.pow)

    def __rpow__(self, other):
        return self.binary_op(other, lambda self_, other_: ops.pow(other_, self_))

    def __lt__(self, other):
        return self.binary_op(other, ops.lt)

    def __gt__(self, other):
        return self.binary_op(other, ops.gt)

    def __le__(self, other):
        return self.binary_op(other, ops.le)

    def __ge__(self, other):
        return self.binary_op(other, ops.ge)

    def binary_op(self, other, op):
        if not callable(other):
            def get_lambda(other_):
                return lambda: other_

            other = on_steroids(get_lambda(other))
        f1_args, f2_args, all_args = arguments_merger(self.call, other.call)

        f1_args_declaration = arg_dict_to_string(f1_args)
        f2_args_declaration = arg_dict_to_string(f2_args)
        all_args_declaration = arg_dict_to_string(all_args)
        code = f"""
def wrapper({all_args_declaration}):
    return op(self({f1_args_declaration}), other({f2_args_declaration}))
"""
        exec_out = {}
        exec(code, {**globals(), **locals()}, exec_out)
        print(exec_out['wrapper'])
        return on_steroids(
            exec_out['wrapper']
        )


@on_steroids
def f1(x, y):
    return x + y


@on_steroids
def f2(y=20, z=10):
    return y + z


print((f1 + f2/f1 - 1)(x=1, y=2))

f1_args, f2_args, all_args = arguments_merger(f1.call, f2.call)
print(arg_dict_to_string(f1_args))
print(arg_dict_to_string(f2_args))
print(arg_dict_to_string(all_args))

