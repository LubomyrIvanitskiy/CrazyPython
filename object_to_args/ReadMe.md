Inappropriate Intimacy - is an anti-pattern where class or function has known (uses) too much about another class/function.

To make the code clearer and less messy we should try to avoid such situations.

For example if we have some data class D with properties x, y, and z, and we have a function foo() which uses only D.x property, 
it is always better to make the function foo(x) vs foo(d: D), because foo does not need D.y, and D.z

This principle is often violated, especially when writing in OOP paradigms.

Passing 'self' as an argument to a method even if the method does not need it, or need to access only single property is an overkilling.

This module help to overcome this problem by providing the mechanism of needed argument selecting from the object provided as argument

Example
```python
import dataclasses

from object_to_args import accept_objects

@dataclasses.dataclass
class Vector:
    x: int
    y: int


@accept_objects         #allows two ways of calling the function: f(x, y) and f.on(object)()
def get_len(x, y):
    return (x ** 2 + y ** 2) ** 0.5


vector1 = Vector(1, 2)
vector2 = Vector(4, 2)

print(
    f"{get_len.on(vector1)()=}",
    f"{get_len(1,2)=}",
    sep="\n"
)                       # will print the same result
```

Pros:
1. Solves "Inappropriate Intimacy"
2. More clear arguments - we can explicitly see which exactly properties are needed for the function
3. Easier to test/mock functions
4. Concurrency safe. Needed arguments are extracted before the function call, so the case when some of properties 
may be changed in the middle of the function by another thread is impossible 