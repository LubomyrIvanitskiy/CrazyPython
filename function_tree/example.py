from types import FunctionType

from function_caller_scope import accessed_by


def f():
    print(x)
    f2()


with accessed_by(f):
    x = 10 + 12


    def f1():
        print("f1 x", x)


    def f2():
        print("f2 y", y)
        f2_1()


    with accessed_by(f2):
        y = 100

        def f2_1():
            print("f2_1 y", x)

f()
#
# for g in dict(**globals()):
#     if isinstance(globals()[g], FunctionType):
#         if '__accessors__' not in globals()[g].__dict__:
#             print(g, 'has no accessors')
#         else:
#             print(g, globals()[g].__accessors__)
