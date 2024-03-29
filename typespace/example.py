from typespace import assert_failed, typed, Object, Or, Collection, overload, configure as typespace_config
from typespace.predefined import Number, Positive, NonZero, Email, CamelStyled

typespace_config(enabled=True)  # DO NOT FORGET TO DISABLE IT FOR PRODUCTION


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


# -------------


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


# - --------------- Test return type --------
# TODO not sure this functionality is needed

@typed
def foo(x: int) -> str:
    return x


assert_failed(foo, 9)


# ------------ Use boolean functions as types

@typed
def send(x: str.isdigit):
    return int(x)


assert send('13341434') == 13341434
assert_failed(send, '13341434L')
