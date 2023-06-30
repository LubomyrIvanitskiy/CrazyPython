from script_args import entrypoint, launch


@entrypoint
def hello(arg):
    print('Hello, world!', arg)


@entrypoint
def bye():
    print('Bye, world!')


if __name__ == '__main__':
    launch()
