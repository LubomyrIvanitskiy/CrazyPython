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
