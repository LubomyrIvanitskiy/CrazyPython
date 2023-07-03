from function_scope import functions

a = 4
b = 5
with functions as math:
    k = 10


    def add(x, y):
        return x + y


    def multi(x, y):
        return x * y


    def combine(x, y):
        return k + add(x, y) + multi(x, y)

print("END", math.combine(3, 4))

