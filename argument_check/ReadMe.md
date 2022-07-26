Python annotations were introduced in v.3.0 and since then are commonly used as type hints. 
But the annotation engine is more than just hints. You can use any object as a variable/argument annotation.

This script shows how to abuse the annotations feature to provide a simple and intuitive mechanism for validating function input arguments.

Example:
```python
from __future__ import annotations

import math

from argument_check import restricted


########################
# Simple condition check
########################

@restricted
def sqrt(x: x >= 0):
    return math.sqrt(x)


print(f"{sqrt(9)=}")
try:
    print(f"{sqrt(-4)=}")
except AssertionError as e:
    print("Error", e)
    
# >>> sqrt(9)=3.0
# >>> Error x >= 0 is False


##############################
# Multiple checks per argument
##############################


@restricted
def get_hex_color(r: "int, r<256", g: "int, g<256", b: "int, b<256") -> "dcv":
    return '#%02x%02x%02x' % (r, g, b)


print("Selected color:", get_hex_color(4, 122, 200))
try:
    print("Selected color:", get_hex_color(4, 122, 3000))
except AssertionError as e:
    print("Error", e)

# >>> Selected color: #047ac8
# >>> Error b<256 is False


############################################
# Referencing other arguments while checking
############################################

@restricted
def create_range(
        start: int,
        end: "int, end > start",
        step: "int, step < (end - start), (end - start) % step == 0"
):
    i = start
    while i < end:
        yield i
        i += step


print(f"{list(create_range(0,100,20))=}")
try:
    print(f"{list(create_range(0,100,30))=}")
except AssertionError as e:
    print("Error", e)

# >>> list(create_range(0,100,20))=[0, 20, 40, 60, 80]
# >>> Error (end - start) % step == 0 is False
```