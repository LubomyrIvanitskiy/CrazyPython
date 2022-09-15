Imagine you are writing the an API class that makes requests to the server and receives responces.

```python
class API:
    def _save_to_db(self, response):
        ...

    def make_request(self):
        ...
        self.on_success(Response("Success"))

    def on_success(self, response):
        self._save_to_db(response)
```

Now, when the request succeed you would like to notify a client via a callback mechanism, so you add a callback to the
class

```python
class API:
    def __init__(self, callback: Callback):
        self.callback = callback  # <-- Here

    def _save_to_db(self, response):
        ...

    def make_request(self):
        ...
        self.on_success(Response("Success"))

    def on_success(self, response):
        self.callback.on_success(response)  # <-- Here
        self._save_to_db(response)
```

What bad could happen?

The bad thing is that the callback receives response as its argument.
The response is mutable.
So, if the client is careless, he can occasionally mutate the response (for ex. response.message = "fake message").
As the result the wrong data will be stored to the database!
Not good...

How can we avoid such scenario?

Using this package you can define your `response` argument as a read-only in the callback interface.
So if somebody tries to mutate it - the runtime error will occur. The explicit error is always better than hidden
implicit silent bug.

### Steps

1. Define the callback protocol

```python
class Callback(
    metaclass=AccessGuard):  # AccessGuard enforce all subclass methods to have the same signature as the base ones 

    @control_access  # @control_access ensures that the function will raise an exception if someone tries to modify the argument marked by Read type
    def on_success(self, result: Read[
        Response]):  # Read[Response] mean the function can only read response attributes. There are also Write, Exec and other types available
        pass
```

2. Ensure the client side subclassed the Callback protocol

```python
class API:
    def __init__(self, callback: Callback):
        assert isinstance(callback, Callback)
        self.callback = callback  # <-- Here
```

3. Enjoy less buggy codebase

Now if somebody tries to inject some bad stuff into your `response` he will be disappointed.

```python
class UserCallback(Callback):

    def on_success(self, result):
        result.msg = "Fake message"         # will raise an error
        print(result)
```

### Notes

Supported access types:

1. `something: Read[Something]` - means the function can only access the Something instance variable.
    1. `something.x` - allowed
    2. `something.x = 10` - raise an error
2. `something: Write[Something]` - the function disallowed to read from the Something instance. The only variable
   setting is allowed
    1. `something.x` - raise error
    2. `something.x = 10` - allowed.
3. `something: Exec[Something]`
    1. `something.x` - rainse an error
    2. `something.x = 10` - raise an error
    3. `something()` or `something.foo()` - allowed
4. `something: ReadWrite[Something]` - self-explanatory
5. `something: ReadExec[Something]` - self-explanatory
6. `something: WriteExec[Something]` - self-explanatory
7. `something: ReadWriteExec[Something]` - self-explanatory
8. `something: BlackBox[Something]` - no operations allowed on the object. Only passing it as-is to another function is
   allowed

Note: if a function declares all its arguments as a read-only - it is considered as read-only function, and so, it is
allowed to be run even without Execution permissions

### TODO:
Add support for `__setitem__` and `__delitem__` as a Write-operations as well as for the `__setitem__` as a Write operation

