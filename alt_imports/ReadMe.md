Run

```shell
python setup.py sdist
pip install sdist/CrazyPython-0.0.0.tar.gz
```

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

>>> from tags.math import *
>>> add(2,2)
>>> diff(2,2)
4
```