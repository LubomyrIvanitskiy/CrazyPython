Run

```shell
python setup.py sdist
pip install sdist/CrazyPython-0.0.0.tar.gz
```
Add empty `__manifest__.py` file to your root project dir
```python
# Module1
>>> from tags import tag
...
... @tag("math")
... def add(a, b):
...    return a+b
...
# Module2
>>> from tags import tag
...
... @tag("math")
... def diff(a, b):
...    return a-b
...

Add imports of all modules that used `tag` decorator to `__manifest__.py' like:

#__manifest__.py
... import some_module1
... import some_module2

Now you can youse you alt imports!

>>> from tags.math import *
>>> add(2,2)
4
>>> diff(2,2)
0
```

The module allow assign different tags for functions. Those tags can be used as alternative import path for better and more handy function grouping.

Single function can have multiple tags.

So, the same function, for example, may be imported in different ways:
1. from original.package import validate_number
2. from tags.features.login_flow import validate_number
3. from tags.utils.string import validate_number

Feel free to contribute and/or open issues!

**NOTE**: You will need to create a __manifest__.py file where all modules that use tags decorator should be put in order to make it working
