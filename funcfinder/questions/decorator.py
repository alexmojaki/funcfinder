from __future__ import absolute_import
from funcfinder.utils import *
import inspect


def decorator_with_introspection(func):
    """
    Given a function and a decorator
    (a function with a function as an argument that returns a wrapped/wrapper function),
    apply the decorator to the function (i.e. return the decorated function)
    without affecting the ability to perform introspection on the original function, i.e. check its name,
    signature (argument count), source, etc.
    """
    def decorator(function):
        def double_wrapper(*args):
            return function(*args) * 2
        return double_wrapper

    def function_with_a_name(a, b, c, d):
        # insert comment here
        return a + b + c + d

    wrapped = func(function_with_a_name, decorator)
    assertEqual(wrapped(1, 2, 3, 4), 20)
    assertEqual(wrapped.__name__, "function_with_a_name")
    assertEqual(wrapped.func_code.co_argcount, 4)
    assertIn("# insert comment here", inspect.getsource(wrapped))
