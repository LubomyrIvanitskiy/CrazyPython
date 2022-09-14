import dataclasses

from without_self import NoSelf, noself


# noinspection PyMethodParameters
class A:

    def __init__(self):
        self.x = 1
        self.y = 2

    @noself  # Example of making a specific method as `noself` method
    def foo(self_x, self_y):
        return self_x + self_y


# noinspection PyMethodParameters
@dataclasses.dataclass
class B(metaclass=NoSelf):  # Example of making all class methods as `nonself`
    msg: str

    def boo(self_msg):
        return f"I am B's boo() with message: {self_msg}"


a = A()
print(
    f"{a.foo()=}",          # Here the self_x and self_y are automatically obtained from the a instance
    f"{A.foo(1, 2)=}",      # Sure, you can also define the arguments manually if you want
    f"{B('hi').boo()=}",
    sep="\n"
)

# a.foo()=3
# A.foo(1, 2)=3
# B('hi').boo()="I am B's boo() with message: hi"
