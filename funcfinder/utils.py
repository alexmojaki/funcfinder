from itertools import izip_longest
import importlib


def solves(*questions):
    """
    Indication that this function satisfies the tests in `questions`.
    """

    def real_decorator(answer):
        answer.solved_questions = questions
        for question in questions:
            question.answers = getattr(question, "answers", []) + [answer]
        return answer

    return real_decorator


def ask_ignore(answer):
    answer.ask_ignore = True
    return answer


def try_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        return _ModulePlaceholder(TryImportError(e))


class _ModulePlaceholder(object):

    def __init__(self, exc):
        self.exc = exc

    def __getattribute__(self, item):
        raise object.__getattribute__(self, "exc")


class TryImportError(ImportError):
    pass


def assertTrue(expr):
    assert expr


def assertFalse(expr):
    assert not expr


def assertEqual(a, b):
    assert a == b


def assertNotEqual(a, b):
    assert a != b


def assertIs(a, b):
    assert a is b


def assertIsNot(a, b):
    assert a is not b


def assertIsNone(a):
    assert a is None


def assertIsNotNone(a):
    assert a is not None


def assertIn(a, b):
    assert a in b


def assertNotIn(a, b):
    assert a not in b


def assertIsInstance(a, b):
    assert isinstance(a, b)


def assertIsNotInstance(a, b):
    assert not isinstance(a, b)


def assertAlmostEqual(a, b):
    assert round(a - b, 7) == 0


def assertNotAlmostEqual(a, b):
    assert round(a - b, 7) != 0


def assertEqualIters(a, b):
    """
    Assert that two iterables have equal elements in order, whether they are lists, tuples, strings, iterators, etc.
    For example
    assertEqual([1, 2, 3], (1, 2, 3))
    will fail but
    assertEqualIters([1, 2, 3], (1, 2, 3))
    will pass.
    This is a shallow comparison: for nested iterables use assertDeepEqualIters.
    """
    assert all(i1 == i2 for i1, i2 in izip_longest(a, b, fillvalue=object()))


def assertDeepEqualIters(a, b):
    """
    Assert that nested iterables have equal elements in order, regardless of iterable type
    like assertEqualIters, but arbitrarily deep and regardless of structure.
    For example,
    ["ab", "cd", "ef", "gh", 1, [[[2]]]]
    is not equal to
    ["ab", ["c", "d"], ("e", "f"), (c for c in "gh"), 1, [[[2]]]]
    not even according to assertEqualIters, but according to this function they are.
    """
    try:
        iter(a)
    except TypeError:
        assert a == b
    else:

        # Avoid infinite recursion for single character strings
        if isinstance(a, basestring) and len(a) == 1:
            assert a == b
            return

        for i1, i2 in izip_longest(a, b, fillvalue=object()):
            assertDeepEqualIters(i1, i2)


def assertRaises(callableObj=None, *args):
    """
    Fail unless an exception is raised by callableObj when invoked
    with arguments args.

    If called without arguments, will return a context object used like this::

        with assertRaises():
            do_something()
    """
    context = _AssertRaisesContext()
    if callableObj is None:
        return context
    with context:
        callableObj(*args)


class _AssertRaisesContext(object):
    """A context manager used to implement assertRaises"""

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, _exc_value, _tb):
        assert exc_type is not None
        return True
