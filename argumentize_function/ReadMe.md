**Argumentize** decorator allow convert any function into kind a 'pure' function that eliminate all globals and closures
as
a implicit dependencies but allow them to be passed as regular key-value arguments.

Here is a simple example:

```python
from argumentize import argumentize

x = 100


def foo(a, b, c):
    return a + b + c + x


foo = argumentize(foo)

foo(1, 2, 3)  # 106
foo(1, 2, 3, x=10)  # 16
```

Argumentized can be any dependency not only a variable. Here is how you can use it with a function:

```python
from argumentize import argumentize


def foo(a, b, c):
    return a + b + c


def bar(a, b, c, d):
    return foo(a, b, c) + d


bar = argumentize(bar)

bar(1, 2, 3, 4)  # 10

bar(1, 2, 3, 4, foo=lambda a, b, c: a * b * c)  # 24
```

Argumentize can be used as a decorator:

```python

from argumentize import argumentize


@argumentize
def foo(a, b, c):
    return a + b + c


foo(1, 2, 3)  # 6

foo(1, 2, 3, b=10)  # 14
```

If you does not provide the value for argumented argument the default variable (either from globals or from the function
closure) will be used