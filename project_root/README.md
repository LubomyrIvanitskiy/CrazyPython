Tool for running CWD-agnostic Python scripts. 

With this module you can run your script from **any project nested folder without breaking your imports** (including relative imports).

```shell
pip install root-relative
python -m root_relative package1.module1
```

This line will try to find the module automatically and detect the project root folder based on the module name provided.
After that the CWD is automatically changed and the module is run as-a-module from the project root.

Also, there is a fix for relative import uncertainty.

If there a/b/c/d and a/b are both added to the sys.path. As a result, if you have a module inside a/b/c/d - you will have two options to import this module
```python
import a.b.c.d.module
# or 
import c.d.module
```
The both options will import the module but relative imports will work differently for them.

In the first case you can easily use 
```python
from ... import another_module
```
but for the second case you'll have 
```python
ImportError: attempted relative import beyond top-level package
```

This module fixes this error by hooking the import process and always selecting the longer module path if multiple paths are provided.
