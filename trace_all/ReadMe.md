# Code Tracing with Script Args

This repository contains a Python script for code tracing. The script allows you to trace the execution of a Python module and display code lines along with variable changes during the execution.

# Example of program output on simple Fibonachi numbers script

```shell
>> Start Tracing File "trace_all\example.py", line 1
>>  0                                                                                       # {}                                                                                                                                                                                                      
--------------------------------------------------------------------------------
## CALLSTACK:
##	trace_all\example.py:<module> ->
##	trace_all\example.py:<module>() File "trace_all\example.py", line 1

>>  1      n = 10                                                                           # {}                                                                                                                                                                                                      
>>  1      n = 10                                                                           # {'n': 10}                                                                                                                                                                                               
>>  2      num1 = 0                                                                         # {'num1': 0}                                                                                                                                                                                             
>>  3      num2 = 1                                                                         # {'num2': 1}                                                                                                                                                                                             
>>  4      next_number = num2                                                               # {'next_number': 1, 'num2': 1}                                                                                                                                                                           
>>  5      count = 1                                                                        # {'count': 1}                                                                                                                                                                                            
>> 6-7 ...
>>  7      while count <= n:                                                                # {'n': 10, 'count': 1}                                                                                                                                                                                   
1
>>  8          print(next_number)                                                           # {'next_number': 1}                                                                                                                                                                                      
>>  9          count += 1                                                                   # {'count': 2}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 1, 'num2': 1, 'num1': 1}                                                                                                                                                                
>>  11         next_number = num1 + num2                                                    # {'next_number': 2, 'num2': 1, 'num1': 1}                                                                                                                                                                
>>  7      while count <= n:                                                                # {'n': 10, 'count': 2}                                                                                                                                                                                   
2
>>  8          print(next_number)                                                           # {'next_number': 2}                                                                                                                                                                                      
>>  9          count += 1                                                                   # {'count': 3}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 2, 'num2': 2, 'num1': 1}                                                                                                                                                                
>>  11         next_number = num1 + num2                                                    # {'next_number': 3, 'num2': 2, 'num1': 1}                                                                                                                                                                
>>  7      while count <= n:                                                                # {'n': 10, 'count': 3}                                                                                                                                                                                   
3
>>  8          print(next_number)                                                           # {'next_number': 3}                                                                                                                                                                                      
>>  9          count += 1                                                                   # {'count': 4}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 3, 'num2': 3, 'num1': 2}                                                                                                                                                                
>>  11         next_number = num1 + num2                                                    # {'next_number': 5, 'num2': 3, 'num1': 2}                                                                                                                                                                
>>  7      while count <= n:                                                                # {'n': 10, 'count': 4}                                                                                                                                                                                   
5
>>  8          print(next_number)                                                           # {'next_number': 5}                                                                                                                                                                                      
>>  9          count += 1                                                                   # {'count': 5}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 5, 'num2': 5, 'num1': 3}                                                                                                                                                                
>>  11         next_number = num1 + num2                                                    # {'next_number': 8, 'num2': 5, 'num1': 3}                                                                                                                                                                
>>  7      while count <= n:                                                                # {'n': 10, 'count': 5}                                                                                                                                                                                   
8
>>  8          print(next_number)                                                           # {'next_number': 8}                                                                                                                                                                                      
>>  9          count += 1                                                                   # {'count': 6}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 8, 'num2': 8, 'num1': 5}                                                                                                                                                                
>>  11         next_number = num1 + num2                                                    # {'next_number': 13, 'num2': 8, 'num1': 5}                                                                                                                                                               
>>  7      while count <= n:                                                                # {'n': 10, 'count': 6}                                                                                                                                                                                   
13
>>  8          print(next_number)                                                           # {'next_number': 13}                                                                                                                                                                                     
>>  9          count += 1                                                                   # {'count': 7}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 13, 'num2': 13, 'num1': 8}                                                                                                                                                              
>>  11         next_number = num1 + num2                                                    # {'next_number': 21, 'num2': 13, 'num1': 8}                                                                                                                                                              
>>  7      while count <= n:                                                                # {'n': 10, 'count': 7}                                                                                                                                                                                   
21
>>  8          print(next_number)                                                           # {'next_number': 21}                                                                                                                                                                                     
>>  9          count += 1                                                                   # {'count': 8}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 21, 'num2': 21, 'num1': 13}                                                                                                                                                             
>>  11         next_number = num1 + num2                                                    # {'next_number': 34, 'num2': 21, 'num1': 13}                                                                                                                                                             
>>  7      while count <= n:                                                                # {'n': 10, 'count': 8}                                                                                                                                                                                   
34
>>  8          print(next_number)                                                           # {'next_number': 34}                                                                                                                                                                                     
>>  9          count += 1                                                                   # {'count': 9}                                                                                                                                                                                            
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 34, 'num2': 34, 'num1': 21}                                                                                                                                                             
>>  11         next_number = num1 + num2                                                    # {'next_number': 55, 'num2': 34, 'num1': 21}                                                                                                                                                             
>>  7      while count <= n:                                                                # {'n': 10, 'count': 9}                                                                                                                                                                                   
55
>>  8          print(next_number)                                                           # {'next_number': 55}                                                                                                                                                                                     
>>  9          count += 1                                                                   # {'count': 10}                                                                                                                                                                                           
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 55, 'num2': 55, 'num1': 34}                                                                                                                                                             
>>  11         next_number = num1 + num2                                                    # {'next_number': 89, 'num2': 55, 'num1': 34}                                                                                                                                                             
>>  7      while count <= n:                                                                # {'n': 10, 'count': 10}                                                                                                                                                                                  
89
>>  8          print(next_number)                                                           # {'next_number': 89}                                                                                                                                                                                     
>>  9          count += 1                                                                   # {'count': 11}                                                                                                                                                                                           
>>  10         num1, num2 = num2, next_number                                               # {'next_number': 89, 'num2': 89, 'num1': 55}                                                                                                                                                             
>>  11         next_number = num1 + num2                                                    # {'next_number': 144, 'num2': 89, 'num1': 55}                                                                                                                                                            
>>  7      while count <= n:                                                                # {'n': 10, 'count': 11}                                                                                                                                                                                  

>> 8-12 ...
>>  12     print()                                                                          # {}                                                                                                                                                                                                      
>> () <-- <module>()
>>-------------------------------------------------------------------------------- 
>> [CONTINUE] ():
>>  0                                                
```

## Prerequisites

Before using the script, make sure you have the following dependencies installed:

- Python (version 3.6 or higher)
- `script_args` library (install using `pip install script-args`)
- `pygments` library (install using `pip install pygments`)

## Installation

1. Clone the repository to your local machine:

```shell
git clone https://github.com/your-username/code-tracing.git
```


2. Install the required dependencies:

```shell
pip install script-args
pip install pygments
```


## Usage

## From Concsole
You can use the script from commandline by providing module name you want to trace:
```shell
python your_script.py -bg light -cs 100 -vs 250 -t your_module.some_function[10:20]
```
### Command-line Arguments

* -bg: Specify the background color for the code output (default: 'dark').
* -ip: Include private variables in the tracing (default: False).
* -ib: Include built-in variables in the tracing (default: False).
* -il: Include external libraries in the tracing (default: False).
* -t: Specify the targets to trace in the format 'file_name.function_nameline_from:line_to' (optional).
* -cs: Set the code line width for the output (default: 80).
* -vs: Set the variables display width for the output (default: 200).

## Programatically
Also you can use it programattically by following these steps:
1. Import the script and the tracing function in your Python module:

```python
from trace_all import tracing
```

1. Decorate your main function with the @entrypoint decorator from script_args. This will allow you to pass command-line arguments to your script:
```python
from script_args.script_args import entrypoint

@entrypoint(
    background='-bg',
    include_privates='-ip',
    include_builtins='-ib',
    include_libs='-il',
    targets='-t',
    code_size='-cs',
    vars_size='-vs',
)
def main(module: str, home: str = os.getcwd(),
         include_privates: bool = False,
         include_builtins: bool = False,
         include_libs: bool = False,
         targets: tuple[str] = None,
         var_mode: str = 'used+',  # diff, used, all, none
         background: str = 'dark',
         code_size: int = 80,
         vars_size: int = 200):
    # Your main function code goes here
    pass
```

2. Within your main function, use the tracing context manager to enable code tracing:
```python
if __name__ == '__main__':
    with tracing(
            home=home,
            include_privates=include_privates,
            include_builtins=include_builtins,
            include_libs=include_libs,
            targets=targets,
            var_mode=var_mode,
            background=background,
            code_size=code_size,
            vars_size=vars_size
    ):
        runpy.run_module(module, run_name='__main__')
...
```