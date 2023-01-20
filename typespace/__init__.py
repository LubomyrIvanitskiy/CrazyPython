import ast
import inspect
import builtins
import sys
from collections import defaultdict
from itertools import product

import astor


def _find_expressions(var_names, func, level=None):
    if level is None:
        level = 0
    expressions = {}
    inputs = set()
    tree = ast.parse(inspect.getsource(func))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            target_names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            for var_name in var_names:
                if var_name in target_names:
                    expressions[var_name] = (level, astor.to_source(node.value).strip('\n\r\t '))
                    for dep in ast.walk(node.value):
                        if isinstance(dep, ast.Name) and dep.id != var_name:
                            inps, exprs = _find_expressions([dep.id], func, level + 1)
                            expressions.update(exprs)
                            inputs.update(inps)
    for var_name in var_names:
        if var_name not in expressions:
            inputs.add(var_name)

    return inputs, expressions


def find_expressions(var_names, func):
    inps, exprs = _find_expressions(var_names, func)
    return inps, _sort_expressions(exprs)


def _sort_expressions(expressions):
    return [f'{e[0]}={e[1][1]}' for e in sorted(expressions.items(), key=lambda item: item[1][0], reverse=True)]


def find_assert_variables(func):
    asserts = list()
    tree = ast.parse(inspect.getsource(func))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            assert_vars = set()
            for dep in ast.walk(node.test):
                if isinstance(dep, ast.Name) and dep.id not in vars(builtins):
                    assert_vars.add(dep.id)
            expr = astor.to_source(node.test).strip(' \n\t\r')
            asserts.append(
                ('assert ' + expr + (f", '{node.msg.value}'" if node.msg else f", '{expr}'"), assert_vars))
    return asserts


def validate(init_expressions, assert_expression, kwargs):
    for e in init_expressions + [assert_expression]:
        if not e.endswith('='):
            exec(e, globals(), kwargs)


class ContextDecorator:

    def __init__(self, decorator):
        self.decorator = decorator

    def __enter__(self):
        self.enter_locals = dict(**sys._getframe(0).f_back.f_locals)
        return self.decorator.types

    def __exit__(self, exc_type, exc_val, exc_tb):
        exit_locals = sys._getframe(0).f_back.f_locals
        new_funcs = set(f for f in exit_locals if f not in self.enter_locals if inspect.isfunction(exit_locals[f]))
        exit_locals.update({
            f_name: self.decorator(exit_locals[f_name]) for f_name in new_funcs
        })

    def __call__(self, func):
        return self.decorator


def typespace(space_def):
    if not hasattr(space_def, 'funcs'):
        space_def.funcs = defaultdict(list)

    assertions = []
    asserts = find_assert_variables(space_def)
    for a_expr, a_vars in asserts:
        inputs, assert_expressions = find_expressions(a_vars, space_def)
        assertions.append((a_expr, inputs, assert_expressions))

    def decorator(func):
        sig = inspect.signature(func)
        inv_annotations = defaultdict(list)
        for name, annotation in func.__annotations__.items():
            for a_i in annotation.split(' '):
                inv_annotations[a_i].append(name)

        def header(*args, **kwargs):
            arguments = sig.bind(*args, **kwargs).arguments
            for assertion, inputs, init_expressions in assertions:
                if any(v not in inv_annotations for v in inputs):
                    continue
                for prod in product(*(inv_annotations[k] for k in inputs)):
                    kwarg = {annotation: arguments[var_name] for annotation, var_name in zip(inputs, prod)}
                    try:
                        validate(init_expressions, assertion, kwarg)
                    except AssertionError as e:
                        return e
            return None

        space_def.funcs[func.__name__].append((header, func))

        def wrapper(*args, **kwargs):
            for head, fun in space_def.funcs[func.__name__]:
                error = head(*args, **kwargs)
                if error is None:
                    return fun(*args, **kwargs)
            raise error

        return wrapper

    decorator.__name__ = space_def.__name__

    decorator.__dict__['types'] = list(inspect.signature(space_def).parameters.keys())
    # for k in list(inspect.signature(space_def).parameters.keys()):
    #     decorator.__dict__[k] = k

    return decorator
