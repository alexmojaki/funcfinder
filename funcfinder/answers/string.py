from __future__ import absolute_import
import funcfinder.questions.string as q
from funcfinder.utils import solves


@solves(q.format_without_nones)
def format_without_nones(format_string, args):
    return format_string.format(*("" if arg is None else arg for arg in args))

