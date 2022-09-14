All class methods should define self as their first argument.

But why? What if I don't need any of the object data? Or what if I need just a single object's property?

Passing the object with 100500 properties into the function when you need only few of that properties considered to be
a "bad smell".

Disadvantages of such approach:
1. It is not clear from the function signature which of the `self` properties will be used in the function.
2. Passing self as an argument allow arbitrary function to change the self state, which is not always required behaviour
3. `self` is a mutable object. So you have no guarantee that the self.x at the beginning of the function is the same as self.x in the end of it. 
This fact becomes especially danger in multithread apps 
4. Hard to test. You need to mock the whole class instance in order to test the function

This module suggests the new approach of writting OOP classes.

Instead of passing `self` each time you declare a class method - pass the only arguments that are actually needed
for the function work.
If you want some arguments to be automatically obtained from the class instance the method is called on - add `self_` prefix
before such arguments

Example:
```python
import dataclasses

from without_self import NoSelf, noself


# noinspection PyMethodParameters
class A:

    def __init__(self):
        self.x = 1
        self.y = 2

    @noself                     # Example of making a specific method as `noself` method
    def foo(self_x, self_y):
        return self_x + self_y


# noinspection PyMethodParameters
@dataclasses.dataclass
class B(metaclass=NoSelf):      # Example of making all class methods as `nonself`
    msg: str

    def boo(self_msg):
        return f"I am B's boo() with message: {self_msg}"


a = A()
print(
    f"{a.foo()=}",              # Here the self_x and self_y are automatically obtained from the a instance
    f"{A.foo(1, 2)=}",          # Sure, you can also define the arguments manually if you want
    f"{B('hi').boo()=}",
    sep="\n"
)

# Will print:
# a.foo()=3
# A.foo(1, 2)=3
# B('hi').boo()="I am B's boo() with message: hi"
```
