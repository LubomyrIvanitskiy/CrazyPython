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

For more examples see `example.py` and `predefined.py`

# Note
It's important to keep in mind that this library is using assert statement to check the types of arguments passed to a function. If the assertion fails, an AssertionError is raised, this will stop the execution of the program.

# Contribution
All contributions are welcome, feel free to create pull requests.