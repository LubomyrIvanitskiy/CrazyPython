from script_args import entrypoint, launch


@entrypoint(arg='-a')
def hello(arg: str):
    print('Hello, world!', arg)


@entrypoint
def bye():
    print('Bye, world!')


if __name__ == '__main__':
    launch(globals())
