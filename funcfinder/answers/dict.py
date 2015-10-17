from __future__ import absolute_import
import collections

import funcfinder.questions.dict as q
from funcfinder.utils import *
sortedcontainers = try_import("sortedcontainers")


@solves(q.group_by_key_func)
def group_by_key_func(iterable, key_func):
    result = collections.defaultdict(list)
    for item in iterable:
        result[key_func(item)].append(item)
    return result


@solves(q.sort_dict_by_key)
def ordered_dict_sorted_by_key(d):
    return collections.OrderedDict(sorted(d.items()))


@solves(q.sort_dict_by_key, q.always_sorted_dict_by_key)
def sorted_dict(d):
    return sortedcontainers.SortedDict(d)


@solves(q.sort_dict_by_value)
def ordered_dict_sorted_by_value(d):
    return collections.OrderedDict(sorted(d.items(), key=lambda item: item[1]))


@solves(q.copy_dict)
def copy_dict(d):
    return d.copy()
