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
