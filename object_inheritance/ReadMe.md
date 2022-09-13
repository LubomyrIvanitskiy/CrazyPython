All we are familar with concept of inheritance in the OOP paradigm:
the new child class automatically receives all the properties and methods from the parent class.

Python allow to perform inferitance on the class level only. But what about instances?
Having object `a` what if I want to have exact same object `b` but with some property value overridden or added?

For sure, we can achieve this by making the object copy and then overwriting some values.
But we cannot add new values.
Also what if we want to combine multiple object& What if they have different types?

To handle all this situation this module was implemented.

Example:

```python
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
# will print:
# d.x=10
# d.y=100
# d.z=3
# d.k=500
# I am Data1 foo. My x is 10
```

As you can se from the example, d1.x and d2.y value were overwritten by d2.x and d2.y accordingly, the new k attribute
was added.

Also pay attention at the foo() function result. foo() function is defined in the Data1 class but it's `self` argument
is replaced by the
extended object that is why it prints x as 10 not a 1
