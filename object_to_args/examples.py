import dataclasses

from object_to_args import accept_objects


@dataclasses.dataclass
class Vector:
    x: int
    y: int


@accept_objects
def get_len(x, y):
    return (x ** 2 + y ** 2) ** 0.5


def compare_vector_lens(vector1, vector2):
    return get_len.on(vector1)() - get_len.on(vector2)()


vector1 = Vector(1, 2)
vector2 = Vector(4, 2)

print(
    f"{get_len.on(vector1)()=}",
    f"{get_len.on(vector2)()=}",
    f"{get_len(10,20)=}",
    sep="\n"
)
print(
    compare_vector_lens(vector1, vector2)
)
