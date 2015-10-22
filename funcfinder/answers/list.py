from __future__ import absolute_import
import itertools

import funcfinder.questions.list as q
from funcfinder.utils import solves


@solves(q.transpose)
def transpose_with_zip(arr):
    return zip(*arr)


@solves(q.transpose)
def transpose_with_map(arr):
    return map(None, *arr)


@solves(q.transpose_without_tuples, q.transpose)
def transpose_without_tuples(arr):
    return map(list, itertools.izip(*arr))


@solves(q.flatten_2d_list_to_iterable)
def flatten_2d_list_using_generator_comprehension(lists):
    return (x for sublist in lists for x in sublist)


@solves(q.flatten_2d_list_to_iterable)
def flatten_2d_list_to_iterable_using_chain(lists):
    return itertools.chain.from_iterable(lists)


@solves(q.flatten_2d_list_to_iterable, q.flatten_2d_list_to_list)
def flatten_2d_list_using_list_comprehension(lists):
    return [x for sublist in lists for x in sublist]


@solves(q.flatten_2d_list_to_iterable, q.flatten_2d_list_to_list)
def flatten_2d_list_to_list_using_chain(lists):
    return list(flatten_2d_list_to_iterable_using_chain(lists))


@solves(q.contains_all)
def contains_all_using_imap(container, contained):
    return all(itertools.imap(container.__contains__, contained))


@solves(q.contains_all)
def contains_all_using_generator(container, contained):
    return all(x in container for x in contained)
