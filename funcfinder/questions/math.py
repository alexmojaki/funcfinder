from __future__ import absolute_import
from funcfinder.utils import *


def is_divisible_by(func):
    """
    Returns True if the first number is divisible by the second, otherwise False.
    """
    assertTrue(func(4, 2))
    assertTrue(func(6, 2))
    assertTrue(func(6, 3))
    assertTrue(func(9, 3))
    assertFalse(func(4, 3))
    assertFalse(func(9, 2))

    assertTrue(all(func(x, 1) for x in xrange(20)))
    assertTrue(all(func(120, x) for x in xrange(1, 7)))
    assertFalse(func(120, 7))


def is_even(func):
    """
    Returns True if the number is even, otherwise False.
    """
    assertTrue(func(2))
    assertFalse(func(3))
    assertTrue(func(4))

    assertTrue(func(2.0))
    assertFalse(func(3.0))
    assertTrue(func(4.0))

    even = True
    for i in xrange(-100, 100):
        assertEqual(func(i), even)
        even = not even
