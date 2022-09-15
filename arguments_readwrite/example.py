import dataclasses

from arguments_readwrite import Read, control_access, Write, BlackBox, ReadWriteExec, Exec, WriteExec, \
    obtain_access_control


@dataclasses.dataclass
class NestedData:
    x: int


@dataclasses.dataclass
class Data:
    a: int
    b: int
    c: int
    d: NestedData

    def read_only_fun(self: Read["Data"]):
        print("I am foo")


@control_access
def do_something(data: Read[Data]):
    print("Doing something")
    data.read_only_fun()


do_something(Data(1, 2, 3, NestedData(4)))
