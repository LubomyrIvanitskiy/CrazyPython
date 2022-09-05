Run

```shell
python setup.py sdist
pip install sdist/CrazyPython-0.0.0.tar.gz
```

```python
>>> from tags import tag
...
... @tag("math")
... def sum(a, b):
...    return a+b
...

>>> from tags.math import sum
>>> sum(2,2)
4
```