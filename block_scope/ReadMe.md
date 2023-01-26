The <a href="https://en.wikipedia.org/wiki/Scope_(computer_science)#Block_scope"> Block Scope </a> support for
Python <br>

The Block Scope is a mechanism to declare variables that will be available only inside certain 'block' of the code.

Outside this block of code the variables are not accessible (and actually destroyed).

Python supports generator, comprehension, functional, class, module -scopes but not the block scope (like many other
languages like Java, JavaScript, Perl e.t.c)

This module tries to fix this injustice.

Example:

```python
from block_scope import new_scope

a = 4
b = 5
with new_scope() as this:
    this.c = 10                 # you can create new variables inside the block scope
    print("this.a", this.a)     # like other Python scopes this scope can easily access 
                                # the variables declared in the outer scope
    print("this.b", this.b)
    print("this.c", this.c)     # you can access the variables declared withing the block scope
print("this", this)             # will throw the exception like "No attribute 'this'"

```

Enjoy, and Stand With Ukraine!
