Allow functions to be defined inside a function scope that make tham invisible for outer scope that increase code
readability and prevent unintendent access.
It is also handy to group functions in IDE:

![image](https://github.com/LubomyrIvanitskiy/CrazyPython/assets/30999506/464b3123-a8ca-446b-ae5f-01cb2f077935)

![image](https://github.com/LubomyrIvanitskiy/CrazyPython/assets/30999506/02cf28c0-fa50-48c7-91b0-4c2f28608a94)

![image](https://github.com/LubomyrIvanitskiy/CrazyPython/assets/30999506/6f9b679b-c530-4883-b4f9-708cf8577705)

# Advocating

When do I move some code blocks into separate functions?

1. Avoid duplication: When I see that the same code block is used multiple times in different places
2. Detect bottleneck: When the code block looks isolated. Most variables that is defined is no longer needed for the rest of the code
3. Logically Different: If the block looks logically different from the rest of the code and I can describe what the code do in few words without using AND
4. Single Responsibility: When there is single responsibility for this block
5. Test: When I want to have ability to test this block work
6. Need recursion
7. Avoid nesting

The problem is that having a lot of functions inside a module make the module hard to read and understand the purpose for each function.

Function may have different purposes:
1. Using as public API as entry point for the module
2. Helper functions that manage business logic
3. Utils like string manipulations, math e.t.c

How I would like to be able to read the module:

1. See all public API functions
2. Then see all helper functions that helps API functions to work
3. The last thing I am interested in is how utils functions are implemented

To achieve this level of readability - correct function ordering is not enough.
I would like to be able looking at a function to answer the question about it's purpose here.
I need to answer the following questions:
1. Why the function is there
2. Where it is used
3. What is their dependencies
4. Which variable outside it affects

To answer these questions I can use:
1. Docstring
2. CrazyPython/function_tree
3. Arguments hinting (types, CrazyPython/dependent_types) and CrazyPython/argumentize_function
4. CrazyPython/arguments_readwrite