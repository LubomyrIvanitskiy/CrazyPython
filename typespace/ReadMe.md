# Typespace

A Python library that allows for dependent types through the use of function annotations for function arguments.

## Installation (TODO)

To install the library, use pip:

```
pip install typespace
```

## Usage

To use the library, you must first import it:

```python
import typespace
```

You can then use the `@typespace.typed` decorator to annotate the function arguments for which you want to use a
type-test-function.

```python
@typespace.typed
def my_function(arg1: my_type_test_function, arg2: my_type_test_function):
# function body
```

Also, you can use the `@typespace.overload` decorator to define multiple versions of a function with different argument
types.

```python
@typespace.overload
def my_function(arg1: my_type_test_function):
    pass


@typespace.overload
def my_function(arg1: another_type_test_function):
    pass
```

You can also use regular types or classes such as `int`, `float`, `str`, `list`, `tuple`, `dict` as a
type-test-functions.

You can use typespace's helpers functions such as `And`, `Or`, `Xor`, `Not`, `Collection` and `Object` to create more
complex type-test-functions, by combining other type-test-functions together.

You can also use any non-callable non-type Python object as type-test-functions. In this case they will be used as
Literals.

For example

```python
@typed
def f(x: Or('hello', 'Bye'): pass
```

make sense and it will allow 'hello' or 'Bye' literals only

Also you can combine your type-test-functions like:

```python
@typed
def do_something(arr=Collection(Positive, 2, ..., Odd)):
    pass
```

In this case do something will accept the only 4-length collections that has first element positive, second element
equals two, third element - any object and fourth element an Odd number

For more examples see `predefined.py` how to build custom type-test-functions

```python
import re

from typespace import Not, Or, overload, Collection, Object


# ----------- Number Type Examples ------------------

Number = Or(int, float)


def Positive(x: Number):
    assert x > 0


def Negative(x: Number):
    assert x < 0


NonZero = Or(Positive, Negative)


def Odd(x: int):
    assert x % 2 == 1


Even = Not(Odd)


# --------- String Types Example -----------

def Digits(x: str):
    assert x.isdigit()


def Upper(s: str):
    assert s.upper() == s


def Lower(s: str):
    assert s.lower() == s


def CamelStyled(s: str, regex=re.compile(r'^[a-z][a-zA-Z]*$')):
    assert regex.search(s)


def SnakeCased(s: str, regex=re.compile(r'^[a-z_]+$')):
    assert regex.search(s)


def Email(email: str, regex=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')):
    assert regex.search(email)


def Url(s: str, regex=re.compile(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')):
    assert regex.search(s)


# -------------- Structures Example ----------------
@overload
def Point(xy: Collection(int, int)):
    """Applies any 2 integers"""


@overload
def Point(xy: Collection(float, float)):
    """Applies any 2 floats"""


@overload
def Point(xy: Collection(Number, Number)):
    """Applies any 2 numbers (float or int)"""


@overload
def Point(xy: Collection(x=Number, y=Number)):
    """Applies any dictionary like structure with x and y keys and corresponding values with type Number"""

    # This line can be omitted because specified type-tests are empty. This is just for example
    assert Point(xy['x'], xy['y'])


@overload
def Point(xy: Object(x=Number, y=Number)):
    """Applies any object that contains x and y members with Number types"""

    # This line can be omitted because specified type-tests are empty. This is just for example
    assert Point(xy.x, xy.y)


@overload
def Interval(start_end: Collection(Number, Number)):
    assert start_end[0] < start_end[1]


@overload
def Interval(start_end: Collection(x=Number, y=Number)):
    Interval(start_end['x'], start_end['y'])


@overload
def Interval(start_end: Object(x=Number, y=Number)):
    Interval(start_end.x, start_end.y)

```

or `example.py` - example of usage
```python
from typespace import assert_failed, typed, Object, Or, Collection, overload
from typespace.predefined import Number, Positive, NonZero, Email, CamelStyled


# ------- Math --------------
@typed
def square(x: Number):
    return x ** 2


@typed
def sqrt(x: Positive):
    return x ** 0.5


@typed
def div(a: Number, b: NonZero):
    return a / b


# ------------- Math Tests --------------

assert square(-3) == 9

assert_failed(sqrt, -9)

assert div(8, 4) == 2

assert_failed(div, 8, 0)


# -----------------------------------------
# ------------ Overload -------------------

def Google(email: Email):
    assert email.endswith('gmail.com')


def Yahoo(email: Email):
    assert email.endswith('yahoo.com')


@overload
def send_greetings(mail: Yahoo):
    return "Sending to Yahoo user"


@overload
def send_greetings(mail: Google):
    return "Sending to Google user"


# ------------- Overloading Tests --------------
assert send_greetings("user@gmail.com") == "Sending to Google user"
assert send_greetings("user@yahoo.com") == "Sending to Yahoo user"
assert_failed(send_greetings, 'user@unknownmail.com')
```

# Note
It's important to keep in mind that this library is using assert statement to check the types of arguments passed to a function. If the assertion fails, an AssertionError is raised, this will stop the execution of the program.

# Contribution
All contributions are welcome, feel free to create pull requests.