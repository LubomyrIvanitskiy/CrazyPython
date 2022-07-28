Observer pattern is yet another way of implementing listeners in your code. But unlike regular Listeners mechanism, the responsibility of delivering messages is fully taken by a Subject component. 
Also, the Subject is a single component where all events collected together, so you can easily control all your event flow from the single place.

There are plenty of Python libraries/scripts implementing Observer pattern in different way. 

The <a href="https://pypi.org/project/pymitter/">Pymitter library</a> is a good example of them.
But he Pyemitter has few disadvantages:
1. In order to make a function to be an observer you need to have the Subject already created, and mark the function with the corresponding decorator. In real projects it is not always the case.
2. Event emitting allow to pass args and kwargs as without any restrictions about what that arguments should be. So it is easy to declare a function with one set arguments and subscribe it onto some events with another set of parameters which will lead to uncositency in the future
3. No way to subscribe an object with multiple methods
Pros:
1. Async support
2. Wildcard mechanism

This package is an attempt to wrap PyEmitter into another class to fix the cons noted above.

Using this library you'll have:
1. Easy way to subscribe lambdas, functions or even methods onto single or multiple events
2. No ambiguity in the arguments passed. All events have its own type with well documented typped parameters
3. Renamed method for better correspondence to the Observer patter terminology
