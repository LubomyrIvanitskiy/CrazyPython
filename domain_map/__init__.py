import builtins
import logging
from functools import lru_cache
import json

from logging import Logger
from types import FunctionType

import yaml

logger = logging.getLogger(__name__)

LITERAL_TAG = '!literal'
OPTIONAL_TAG = '!optional'
FROM_TAG = '!from'
RESERVED_OPERANDS = {LITERAL_TAG, OPTIONAL_TAG, FROM_TAG}


def split_index(key):
    if not isinstance(key, str):
        return key, None
    if key.strip().endswith(']'):
        index_position = key.index('[')
        key, index = key[:index_position], key[index_position + 1:-1]
        return key, index
    return key, None


def handle_operands(result, operands, path, **kwargs):
    kwargs = dict(json=json.dumps, **builtins.__dict__, **kwargs)
    if operands:
        for op_name in operands[::-1]:
            if op_name in RESERVED_OPERANDS:
                continue
            if not op_name.startswith("!") and not op_name.startswith('?'):
                raise ValueError(f'Unknown operand {op_name}')
            op_type, op_name = op_name[:1], op_name[1:]
            if op_name in kwargs:
                try:
                    operation = kwargs[op_name]
                except Exception as e:
                    logger.debug(e)
                    raise ValueError(f'Error while applying !{op_name} to {result}. {e}')
            else:
                raise ValueError(f'Unknown operand {op_name}')

            if op_type == "!":
                result = operation(result)
            elif op_type == '?':
                if isinstance(operation, type):
                    if not isinstance(result, operation):
                        raise ValueError(f'Expected {operation} got {type(result)} for {path}\'s operand {op_name}')
                elif isinstance(operation, FunctionType):
                    operation_result = operation(result)
                    if not operation_result:
                        raise ValueError(
                            f'Expected {operation} returns {operation_result} for {path}\'s operand {op_name}. Expected non-False result')
            else:
                raise ValueError(f'Unknown operand {op_name} for {path}')
    return result


def _split_operands(s):
    operands, args = [], []
    for part in s.split(' '):
        if part.startswith('!'):
            operands.append(part[1:])
        else:
            args.append(part)
    return operands, ' '.join(args)


def get(source, path, sep='.', indexes=None, **kwargs):
    if indexes is None:
        indexes = {}
    operands, path = _split_operands(path)
    if LITERAL_TAG not in operands:
        parts = path.split(sep)
        result = source
        for part in parts:
            if part.isdigit():
                result = result[int(part)]
            else:
                key, index = split_index(part)
                if index is not None:
                    if index.isdigit():
                        index = int(index)
                    elif index in indexes:
                        index = indexes[index]
                    else:
                        raise ValueError(f'Index {index} is missing in indexes {indexes}')
                    if index < len(result[key]):
                        result = result[key][index]
                    else:
                        raise IndexError(f'Index {index} is out of range')
                else:
                    result = result[key]
    else:
        result = path
    result = handle_operands(result, operands, path, **kwargs)
    return result


def iterate_by_index(source, mapping, by_index, indexes, **kwargs):
    if indexes is None:
        indexes = {}
    by_index_parts = [index.strip() for index in by_index.split('*')]
    i = 0
    while True:
        try:
            if len(by_index_parts) > 1:
                yielded = False
                for item in iterate_by_index(source, mapping, "*".join(by_index_parts[1:]),
                                             indexes={**indexes, by_index_parts[0]: i}, **kwargs):
                    yield item
                    yielded = True
                if not yielded:
                    break
            else:
                if isinstance(mapping, dict):
                    yield mapper(source, mapping=mapping, indexes={**indexes, by_index_parts[0]: i}, **kwargs)
                elif isinstance(mapping, str):
                    yield get(source, mapping, indexes={**indexes, by_index_parts[0]: i}, **kwargs)
        except IndexError as e:
            logger.debug(e)
            break
        i += 1


def mapper(source, *, mapping=None, mapping_path: str = None, indexes=None, **kwargs):
    if mapping_path is not None:
        mapping = read_mapping(mapping_path)
    if isinstance(mapping, dict):
        result = {}
        for k, v in mapping.items():
            key_operands, k = _split_operands(k)
            if FROM_TAG in key_operands:
                get_from = get(source, k.strip(), indexes=indexes)
                result.update(mapper(get_from, mapping=v, indexes=indexes, **kwargs))
                continue
            key, index = split_index(k)
            if index is not None:
                for item in iterate_by_index(source, v, index, indexes, **kwargs):
                    item = handle_operands(item, key_operands, k, **kwargs)
                    result.setdefault(key, []).append(item)
            else:
                if isinstance(v, dict):
                    val = mapper(source, mapping=v, indexes=indexes, **kwargs)
                    val = handle_operands(val, key_operands, k, **kwargs)
                    result[k] = val
                elif isinstance(v, str):
                    optional = False
                    if OPTIONAL_TAG in key_operands:
                        optional = True
                    try:
                        val = get(source, v, indexes=indexes, **kwargs)
                        val = handle_operands(val, key_operands, k, **kwargs)
                        result[k] = val
                    except KeyError as e:
                        if not optional:
                            raise e
                        else:
                            logging.debug(f'WARNING: Key not found: {e}')
                else:
                    # FEATURE: Handling as is
                    v = handle_operands(v, key_operands, k, **kwargs)
                    result[k] = v
    else:
        result = get(source, mapping, indexes=indexes, **kwargs)
    return result


def unknown_constructor(loader, tag_suffix, node):
    print(f"Handling {tag_suffix}")
    if isinstance(node, yaml.MappingNode):
        return loader.construct_yaml_map(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_yaml_seq(node)
    else:
        node.value = f'!{tag_suffix} {node.value}'
        return loader.construct_yaml_str(node)


@lru_cache()
def get_yaml():
    import yaml
    yaml.SafeLoader.add_multi_constructor('!', unknown_constructor)
    return yaml


@lru_cache(maxsize=1)
def read_mapping(path: str):
    if path.endswith('.json'):
        import json
        return json.load(open(path))
    elif path.endswith('.yaml') or path.endswith('.yml'):
        return get_yaml().safe_load(open(path))
