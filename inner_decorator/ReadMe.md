<b>Python decorators</b> is a syntactic sugar that allows you to wrap your existing function into new one adding extra
logic to it.
The most wel known such decorators are:
<li>`@propery` - allows you to access and run an argument-less function as a property
<li>`@lru_cache` - cache function result, so the next time the function is called with the same arguments - the cached result will be returned
<li>`@static_method` - create a static function, so you no longer need to create a class instance to call the function
For more examples take a look at https://github.com/lord63/awesome-python-decorator
<br><br>
But all those decorators behave on the function declaration level only. 

But what if I want to decorate all functions that are used inside a certain "mother" function, keeping them unchanged
for other functions?

This is the reason why this package have been created.
Using `@inner_decorator` you can wrap each function that is used inside the "mother" function. Let's take a look at few
examples:

```python
>> >

def f1():


    ...
return 1
...

>> >

def mother():


    ...
print(f1() + f1())
...

>> > mother()
2
```

Now let's wrap the f1 with some decorator

```python
>> >

def new_f1():


    ...
return 2

>> > from inner_decorator import inner_decorator
>> > mother = inner_decorator(f1=lambda f: new_f1())(mother)
>> > mother()
4
```

For sure instead of running `mother = inner_decorator(f1=lambda f: new_f1())(mother)` you can use @inner_decorator
before declaring the mother function and it will have the same effect

Real world use-cases:
<li> Debugging - when you want to @timeit or print arguments of each function used inside the "mother" function
<li> Mocking inner function result for tests
<li> Changing logic of inner functions of some "mother" function that is declared in a third-party package
<li> Your case

Feel free to suggest improvements and open issues!