Domain mapping is a common task in usual developer routines.
In mathematcs you can easilly map a domain of a vector to another domain.
But doing the same for more complex data structures is not that easy.

This library provides a simple way to map a domain of a data structure to another domain.


## Usage
Imagine you have a structure1 and you want to map it into structure2.

The first thing you should do is to specify the domains of both structures.
Each value in your structure should have a single flat unique key.

Then you need to define a function that will map one key into another.

So the new key will be used as a path to set the value in new structure.

Example:
```python
structure1: dict

structure2: list
```

The first structure is a dictionary, the second is a list we want to map the fisrst structure into.

Let's specify the mapper function that take a dictionary string and convert it into a list index:
```python
def mapper(key: str) -> int:
    return len(key)
```

Now we can map the structure1 into structure2:
```python
from domain_map import map_domain

structure1 = {
    'a': 1,
    'b': 2,
    'c': 3,
}

structure2 = map_domain(structure1, mapper)
```