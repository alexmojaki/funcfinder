from __future__ import absolute_import
import funcfinder.questions.decorator as q
from funcfinder.utils import *

wrapt = try_import("wrapt")


@solves(q.decorator_with_introspection)
def decorator_with_introspection(function, decorator):
    # This is not a great use of the wrapt library as you should place the decorator logic inside here.
    # However it makes it possible to define a generic function.
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return decorator(wrapped)(*args, **kwargs)
    return wrapper(function)
