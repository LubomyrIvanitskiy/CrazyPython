<b>Requires Python 3.8+</b>

Unlike majority of other languages, Python does not support <b>multiline lambda</b> expression. And this really sucks.

But thanks to relatively new Walrus operator there is a hack.

The Walrus Operator was introduced in Python 3.8 (https://docs.python.org/3/whatsnew/3.8.html).
It is not obvious but you can use this operator to "emulate" multiline lambda

```python
lambda: (
    a := 5,
    b := 10,
    c := a + b,
    print(c)
)
```

But the capabilities of such "lambdas" are pretty restricted - there are no ability to use neither loops nor condition
expressions.

What if we'll go further and will add such abilities?

For details take a look at <i>multiline_lambda/example.py</i>

UDP:
The code actually looks ugly (but at least it works:)), so it is not recommended to use it in your daily basis.
But if you really need the "inline function declaration" - you're welcome!
Also, feel free to suggest a nicer solution.