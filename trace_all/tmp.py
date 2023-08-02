import tokenize
import io


def extract_nested_objects(code_str):
    g = tokenize.tokenize(io.BytesIO(code_str.encode('utf-8')).readline)

    nested_objects = []
    current_object = ""

    for tok in g:
        if tok.type == tokenize.NAME:
            if current_object:
                if current_object.endswith('[') or current_object.endswith('.'):
                    current_object += tok.string
                else:
                    nested_objects.append(current_object)
                    current_object = tok.string
            else:
                current_object = tok.string

        elif tok.type == tokenize.OP:
            if tok.string == '.':
                if current_object:
                    current_object += tok.string

            elif tok.string == '[':  # array index access begins
                current_object += tok.string

            elif tok.string == ']':  # array index access ends
                current_object += tok.string

            elif tok.string == ',':  # argument separator
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""
            elif tok.string == '(':  # end of function call or grouping
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""

            elif tok.string == ')':  # end of function call or grouping
                if current_object:
                    nested_objects.append(current_object)
                    current_object = ""

        elif tok.type == tokenize.NUMBER:
            if current_object.endswith('['):  # inside array index access
                current_object += tok.string

    if current_object:
        nested_objects.append(current_object)

    return nested_objects


code_str = 'def trace_off()'
code_str = 'foo(obj.a, 5, arr[m])'
code_str = 'traverse(annotation, arguments[name], __param_name=name) '
code_str = 'self.stack_frame = sys._getframe(0).f_back '
print(extract_nested_objects(code_str))
