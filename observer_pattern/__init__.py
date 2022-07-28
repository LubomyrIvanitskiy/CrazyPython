import inspect
import re
from abc import ABCMeta, abstractmethod
from inspect import isclass
from types import FunctionType
from typing import List, Tuple, Optional

from pymitter import EventEmitter


def _check_event_listener_requirements(func) -> Tuple[bool, Optional[str]]:
    argspec = inspect.getfullargspec(func)
    function_args = argspec.args.copy()
    if "self" in function_args:
        function_args.remove("self")
    if "cls" in function_args:
        function_args.remove("cls")

    if len(function_args) != 1:
        return False, "Function should have single argument (beside self, cls if present) in " \
                      "order to be an event_listener "

    if Event not in argspec.annotations[function_args[0]].__bases__:
        return False, "Function argument should be Event or Event's subclass in order to de an event_listener. " \
                      "Otherwise the function decorator should provide event name as input argument"
    return True, None


def _obtain_event_type(func):
    function_annotation = func.__annotations__.copy()

    arg_name = list(function_annotation)[0]
    arg_type = function_annotation[list(function_annotation)[0]]

    return arg_name, arg_type


def event_listener(func_or_class_or_event_name, event_name=None):
    """
    Decorator to automatically subscribe the function on some event thrown by an EventEmitter
    """
    if isinstance(func_or_class_or_event_name, str):
        return lambda func_or_class: event_listener(func_or_class, event_name=func_or_class_or_event_name)
    func_or_class = func_or_class_or_event_name
    funcs = []
    if not isclass(func_or_class):
        funcs = [func_or_class]
    else:
        class_ = func_or_class
        for func in dir(class_):
            if callable(getattr(class_, func)) and not func.startswith("_"):
                funcs.append(getattr(class_, func))

    for func in funcs:
        if not event_name:
            flag, error_message = _check_event_listener_requirements(func)
            assert flag, error_message

            arg_name, arg_type = _obtain_event_type(func)
            if arg_type == Event:
                func.event_key = "ALL"
            else:
                func.event_key = arg_type.name()
        else:
            func.event_key = event_name

    return func_or_class


class Event:

    @classmethod
    def name(cls):
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name


class EventChannel:
    """
    A class for collecting events and sending them to subscribes
    """

    def __init__(self):
        self.eventEmitter = EventEmitter()

    def notify(self, event: Event):
        self.eventEmitter.emit(event.name(), event)

    def subscribe(self, event_name: str, func: FunctionType):
        self.eventEmitter.on(event_name, func)

    def subscribe_for_all(self, func: FunctionType):
        self.eventEmitter.on_any(func)

    def add_listeners(self,
                      *args,
                      on_all_events=None,
                      **kwargs):
        kwargs["ALL"] = on_all_events
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        _register_listeners(self, *args, **filtered_kwargs)
        return self


def _register_listeners(events: EventChannel, *args, **kwargs):
    """
    Parse the input and automatically subscribe all passed functions or objects on specified events

    May handle few different input types:
        1. Passing functions as positional arguments.
            In such a case the function should contain single argument with Event type or an Event's subtype.
            The function will be subscribed on all events that have the same type as the function argument

            If the argument has type Event (not Event's subclasses) it will be subscribed on all events

        2. Passing functions or lambdas (or list of functions or lambdas) as named arguments
            In this case, each function will be subscribed on all events that have the same name as parameter name.

            if the parameter name is ALL the function will be subscribed on all events

        3. Passing objects as positional arguments
            In this case each object method decorated with @event_listener decorator will be treated as
            a separate function with the rules described in #1


    Parameters
    ----------
    events: EventEmitter
        emitter, we want to be subscribed on
    args: positional argument
        see above
    kwargs: named arguments
        see above

    """
    for a in args:
        if callable(a):
            if "event_key" in a.__dict__:
                events.subscribe(a.event_key, a)
            else:
                # trying to automatically extract event key
                flag, _ = _check_event_listener_requirements(a)
                if flag:
                    arg_name, arg_type = _obtain_event_type(a)
                    events.subscribe(arg_type.name(), a)
                else:
                    raise RuntimeError(f"Function {a} doesn't meet requirements for event_listener. "
                                       f"It should contain single argument that should be an Event or Event's subclass")
        elif isinstance(a, object):
            for func in dir(a):
                # Unlike for function-arguments, the object argument methods must be decorated with @event_listener.
                # That is why we check for event_key here
                if callable(getattr(a, func)) and not func.startswith("_") and "event_key" in getattr(a, func).__dict__:
                    _register_listeners(events, getattr(a, func))
    for k in kwargs:
        if not isinstance(kwargs[k], List):
            value = [kwargs[k]]
        else:
            value = kwargs[k]
        for v in value:
            assert callable(v)
            if k == "ALL":
                events.subscribe_for_all(v)
            else:
                events.subscribe(k, v)
