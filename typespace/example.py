from typespace import typespace


@typespace
def MathSpace(
        Number,
        Positive,
        Negative,
        Odd,
        Even,
        NonZero,
        Degree
):
    assert (isinstance(Number, int) or isinstance(Number, float))
    assert Positive > 0
    assert Negative < 0
    assert Odd % 2 == 1
    assert Even % 2 == 0
    assert NonZero != 0
    assert 0 <= Degree <= 360


@MathSpace
def square(x: 'Number'):
    pass


@MathSpace
def sqrt(x: 'Positive Number'):
    pass


@MathSpace
def div(x: 'Number', y: 'NonZero Number'):
    pass


@MathSpace
def cos(x: 'Degree Number'):
    pass


def tst1():
    try:
        square(19)
        print('square(19) - No Errors')
    except AssertionError as e:
        print("square(19) Error", e)

    try:
        sqrt(-20)
        print('sqrt(-20) - No Errors')
    except AssertionError as e:
        print("sqrt(-20) Error", e)

    try:
        div(20, 0)
        print('div(20, 0) - No Errors')
    except AssertionError as e:
        print("div(20, 0) Error", e)

    try:
        cos(410)
        print('cos(410) - No Errors')
    except AssertionError as e:
        print("cos(410) Error", e)


@MathSpace
def foo(x: 'Positive Number'):
    print("I am positive foo")


@MathSpace
def foo(x: 'Negative Number'):
    print("I am negative foo")


def tst2_polymorphism():
    foo(-30)
    foo(10)


if __name__ == '__main__':
    tst1()
    tst2_polymorphism()
