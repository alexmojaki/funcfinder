from __future__ import absolute_import
from funcfinder.utils import *


def transpose(func):
    """
    Swap/exchange/invert the rows and columns in a list of lists/tuples
    (nested list, 2D list/array, two dimensional list, table, matrix).

    See also transpose_without_tuples.
    """
    assertDeepEqualIters(
        func([[1, 2],
              [3, 4]]),
        [[1, 3],
         [2, 4]]
    )

    assertDeepEqualIters(
        func([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]),
        [[1, 4, 7],
         [2, 5, 8],
         [3, 6, 9]]
    )

    # Doesn't have to be a square
    assertDeepEqualIters(
        func([[1, 2, 3],
              [4, 5, 6]]),
        [[1, 4],
         [2, 5],
         [3, 6]]
    )

    # 200 rows, 100 columns
    assertDeepEqualIters(func([range(100) for _ in xrange(200)]),
                         [[i] * 200 for i in xrange(100)])


def transpose_without_tuples(func):
    """
    Like transpose, but the result consists of lists again, not tuples, i.e. not
    [[1,2], [3,4]] -> [(1,3), (2,4)]
    """
    transpose(func)
    assertEqual(func([[1, 2], [3, 4]]),
                [[1, 3], [2, 4]])


def flatten_2d_list_to_iterable(func):
    """
    Flatten (merge) a list of lists (nested list) into a single iterable, not necessarily a concrete list.
    Only perform a shallow merge, it need not support 3D lists and beyond, or lists with varying depth,
    e.g. [1, 2, [3, 4]].
    Sublists may be different lengths.

    See also flatten_2d_list_to_list.
    """
    assertEqualIters(func([[1]]), [1])
    assertEqualIters(func([[1, 2], [3, 4]]), [1, 2, 3, 4])
    assertEqualIters(func([[0],
                           [1, 2],
                           [3, 4, 5]]),
                     range(6))
    assertEqualIters(func([]), [])

    assertEqualIters(func([[i] for i in xrange(10000)]), xrange(10000))

    before = []
    count = 0
    for i in xrange(1, 100):
        before.append(range(count, count + i))
        count += i
    # before == [[0], [1, 2], [3, 4, 5], ..., [..., count-1]]
    assertEqualIters(func(before), xrange(count))


def flatten_2d_list_to_list(func):
    """
    Flatten a 2D list into an actual list, not just any iterable.
    """
    flatten_2d_list_to_iterable(func)
    assertEqual(func([[1, 2], [3, 4]]), [1, 2, 3, 4])
