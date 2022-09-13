import dataclasses

from object_inheritance import extend


@dataclasses.dataclass
class Data1:
    x: int
    y: int
    z: int

    def foo(self):
        print(f"I am Data1 foo. My x is {self.x}")


@dataclasses.dataclass
class Data2:
    x: int
    y: int


d1 = Data1(1, 2, 3)
d2 = Data2(10, 100)

d = extend(d1, d2)
d.k = 500

print(
    f"{d.x=}",
    f"{d.y=}",
    f"{d.z=}",
    f"{d.k=}",
    sep="\n"
)
d.foo()
