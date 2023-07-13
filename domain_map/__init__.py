import logging

LITERAL_TAG = '!literal'
OPTIONAL_TAG = '!optional'


def split_index(key):
    if not isinstance(key, str):
        return key, None
    if key.strip().endswith(']'):
        index_position = key.index('[')
        key, index = key[:index_position], key[index_position + 1:-1]
        return key, index
    return key, None


def get(source, path, sep='.', indexes=None):
    if indexes is None:
        indexes = {}
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
                    raise ValueError(f'Index {index} is out of range')
            else:
                result = result[key]

    return result


def iterate_by_index(source, mapping, by_index, indexes):
    if indexes is None:
        indexes = {}
    by_index_parts = [index.strip() for index in by_index.split('*')]
    i = 0
    while True:
        try:
            if len(by_index_parts) > 1:
                yielded = False
                for item in iterate_by_index(source, mapping, "*".join(by_index_parts[1:]), indexes={**indexes, by_index_parts[0]: i}):
                    yield item
                    yielded = True
                if not yielded:
                    break
            else:
                if isinstance(mapping, dict):
                    yield mapper(source, mapping, indexes={**indexes, by_index_parts[0]: i})
                elif isinstance(mapping, str):
                    yield get(source, mapping, indexes={**indexes, by_index_parts[0]: i})
        except ValueError:
            break
        i += 1


def mapper(source, mapping, indexes=None):
    if isinstance(mapping, dict):
        result = {}
        for k, v in mapping.items():
            key, index = split_index(k)
            if index is not None:
                for item in iterate_by_index(source, v, index, indexes):
                    result.setdefault(key, []).append(item)
            else:
                if isinstance(v, dict):
                    result[k] = mapper(source, v, indexes)
                elif isinstance(v, str):
                    if v.startswith(LITERAL_TAG):
                        # FEATURE: Handling Literal
                        result[k] = v[len(LITERAL_TAG):].strip()
                    else:
                        optional = False
                        if k.startswith(OPTIONAL_TAG):
                            k = k[len(OPTIONAL_TAG):]
                            optional = True
                        try:
                            result[k] = get(source, v, indexes=indexes)
                        except KeyError as e:
                            if not optional:
                                raise e
                            else:
                                logging.debug(f'WARNING: {e}')
                else:
                    # FEATURE: Handling Literal
                    result[k] = v
    else:
        result = get(source, mapping, indexes=indexes)
    return result
