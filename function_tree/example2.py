from function_tree import accessed_by


def f():
    print(squares)


with accessed_by('f'):
    squares = []
    for a in range(10):
        squares.append(a ** 2)

f() # -> OK

# print(squares)  # rise Exception
