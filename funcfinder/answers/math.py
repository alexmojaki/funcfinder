from __future__ import absolute_import
import funcfinder.questions.math as q
from funcfinder.utils import solves


@solves(q.is_divisible_by)
def is_divisible_by(a, b):
    return a % b == 0


@solves(q.is_even)
def is_even(a):
    return is_divisible_by(a, 2)
