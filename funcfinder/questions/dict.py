from __future__ import absolute_import
import random
import string
import itertools

from funcfinder.utils import *


def group_by_key_func(func):
    """
    Create a dictionary from an iterable such that the keys are the result of evaluating a key function on elements
    of the iterable and the values are lists of elements all of which correspond to the key.
    """
    assertEqual(func("a bb ccc d ee fff".split(), len),
                {1: ["a", "d"],
                 2: ["bb", "ee"],
                 3: ["ccc", "fff"]})

    assertEqual(func([-1, 0, 1, 3, 6, 8, 9, 2], lambda x: x % 2),
                {0: [0, 6, 8, 2],
                 1: [-1, 1, 3, 9]})


def copy_dict(func):
    """
    Returns a new separate dict equal to the original. Updates to the copy don't affect the original.
    """
    original = {'a': 1, 'd': 2, 'b': 3, 'c': 4}
    copy = func(original)

    # An equal but separate copy has been made
    assertEqual(original, copy)
    assertIsNot(original, copy)

    # Usual key access still works
    assertEqual(copy['d'], 2)

    # Deletion works
    del copy['d']
    assertIsNone(copy.get('d'))

    # But it doesn't delete the key in the original
    assertEqual(original['d'], 2)

    # Insertion works
    copy['x'] = 5
    assertEqual(copy['x'], 5)

    # And again, doesn't affect the original
    assertIsNone(original.get('x'))


def sort_dict_by_key(func):
    """
    Return a copy of a dict which still supports all the standard operations with the usual API,
    plus can be iterated over in sorted order by key. Adding keys to the dict may not necessarily preserve this order -
    for that, see always_sorted_dict_by_key.
    """
    copy_dict(func)

    # On my machine at least, this dict does not look sorted
    original_dict = {'a': 0, 's': 1, 'd': 2, 'f': 3}
    sorted_dict = func(original_dict)

    # Iteration is now ordered
    assertEqual(sorted_dict.items(), [('a', 0), ('d', 2), ('f', 3), ('s', 1)])

    # Larger test
    sorted_keys = list(itertools.product(string.ascii_lowercase, string.ascii_lowercase))
    shuffled_keys = list(sorted_keys)
    for i in xrange(10):
        random.shuffle(shuffled_keys)
        original_dict = dict(itertools.izip(shuffled_keys, itertools.count()))
        sorted_dict = func(original_dict)
        assertEqualIters(sorted_keys, sorted_dict.iterkeys())


def always_sorted_dict_by_key(func):
    """
    Return a copied dict sorted by key which preserves its order upon updates.
    """
    sort_dict_by_key(func)
    sorted_dict = func({})
    keys = list(itertools.product(string.ascii_lowercase, string.ascii_lowercase))
    random.shuffle(keys)
    for key in keys:
        sorted_dict[key] = key
        assertEqualIters(sorted(sorted_dict.keys()), sorted_dict.iterkeys())


def sort_dict_by_value(func):
    """
    Return a copy of a dict which still supports all the standard operations with the usual API,
    plus can be iterated over in sorted order by value. Adding keys to the dict may not necessarily preserve this order.
    """
    copy_dict(func)

    # On my machine at least, this dict does not look sorted by value
    original_dict = dict(zip(range(4), "dcba"))
    sorted_dict = func(original_dict)

    # Iteration is now ordered by value
    assertEqual(sorted_dict.items(), [(3, 'a'), (2, 'b'), (1, 'c'), (0, 'd')])

    # Larger test
    sorted_values = list(itertools.product(string.ascii_lowercase, string.ascii_lowercase))
    shuffled_values = list(sorted_values)
    for i in xrange(10):
        random.shuffle(shuffled_values)
        original_dict = dict(itertools.izip(itertools.count(), shuffled_values))
        sorted_dict = func(original_dict)
        assertEqualIters(sorted_values, sorted_dict.itervalues())
