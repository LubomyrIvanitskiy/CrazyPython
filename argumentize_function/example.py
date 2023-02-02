from argumentize_function import argumentize


@argumentize
def do_some_work():
    print("Do this")
    print("Do that")
    print("Check")
    print("Get launch")
    print("Relax")
    print("Do work")
    print(str("Go home"))


print("Regular call:")
do_some_work()

######### Now lets redirect output from print to a logger ##############
import logging

print("\n\nArgumentized call:")
do_some_work(print=lambda *args, **kwargs: logging.warn(" ".join(args)))
print("End")
