# ReadMe.md

## Introducing the Lightweight Command-line Parser for Python Scripts: Script Args

### Introduction

The `script_args` Python module simplifies command-line argument parsing and eliminates the necessity of using `argparse` for most common use cases. It provides a more Pythonic way of dealing with command-line arguments, making your scripts easier to read and maintain.

### How does it work?

Instead of defining command-line arguments in a structured way, `script_args` uses Python functions decorated with `@entrypoint` to define commands. These commands can have typed arguments, which are parsed from the command line.

Let's have a look at a quick example:

```python
from script_args import entrypoint, launch


@entrypoint
def hello(arg: str):
    print('Hello, world!', arg)


@entrypoint
def bye():
    print('Bye, world!')


if __name__ == '__main__':
    launch(globals())

```
Here, two commands (`hello` and `bye`) are defined, each with different arguments. You can call this script from the command line in the following ways:

```bash
python myscript.py hello man
python myscript.py bye
```

The first command will print `Hello, world! man` and the second one will print `Bye, world!`.

Advantages of script_args vs argparse
Simplicity: With script_args, command-line arguments are declared right in the function signature. There's no need for an extra argument-parsing block in your code. This makes your scripts cleaner and easier to understand.

Type Checking: Arguments in script_args are Python-typed, which automatically provides some level of input validation and parsing. For example, an argument declared as int will be automatically converted and validated as an integer.

Flexibility: With argparse, it's common to find yourself writing a lot of boilerplate to support multiple sub-commands. With script_args, each function is its own sub-command, and adding a new one is as simple as defining a new function.

Less Boilerplate Code: argparse requires defining arguments in one place and handling them in another, which often leads to duplication. With script_args, everything is defined in one place, resulting in less code and lower risk of errors.

Functionality: script_args covers a majority of use cases where command line arguments are required. For more complex cases, libraries such as argparse might still be needed.

## Limitations
This tool is a lightweight command-line argument parser and does not currently handle complex scenarios like nested commands or arguments with multiple input types. For such cases, a more robust solution like argparse or click is recommended.

## Conclusion
For simple Python scripts with command-line interfaces, script_args provides a minimalistic and Pythonic alternative to libraries like argparse. Give it a try and see how it can simplify your Python scripting!

**Note**: As of now, this tool doesn't support generating a help menu. You need to provide a clear and detailed documentation for your command-line tool to help users understand how to use the different commands.



