from __future__ import absolute_import
from funcfinder.utils import *


def format_without_nones(func):
    """
    Given a format string in str.format style and a list of arguments, format the string but output an empty string
    for arguments that are None instead of the string 'None'.
    """
    assertEqual(func("{}a{}b{}c{}", [1, None, 2, None]), "1ab2c")
