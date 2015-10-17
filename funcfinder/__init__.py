from bdb import Bdb
import inspect
from itertools import imap, dropwhile, permutations
import pydoc
import re
import sys
import traceback
import timeit

import wrapt

import funcfinder.answers
import funcfinder.questions
from utils import TryImportError


def search_questions(terms):
    if isinstance(terms, basestring):
        terms = terms.split()

    terms = map(str.lower, terms)

    print

    found = False
    for question in funcfinder.questions.functions.itervalues():
        search_string = (question.__name__ + question.__doc__).lower()
        if all(imap(search_string.__contains__, terms)):
            found = True
            print question.__name__ + ":\n"
            print pydoc.getdoc(question)
            print "\n-----------------------\n"

    if not found:
        print "No questions found"


def _show_dependencies(dependencies, existing_sources):
    found_dependency = False
    if dependencies:
        for dependency in dependencies:
            dependency_source = _get_source(dependency)
            if dependency_source in existing_sources:
                continue

            spaceless_dependency_source = re.sub("\s+", "", dependency_source)
            found_matching_source = False
            for existing_source in existing_sources:
                spaceless_existing_source = re.sub("\s+", "", existing_source)
                if spaceless_dependency_source in spaceless_existing_source:
                    found_matching_source = True
                    break
            if found_matching_source:
                continue

            if not found_dependency:
                print "Dependencies:"
                print
                found_dependency = True
            _show_source(dependency, dependency_source)


def show_question(question, time_answers=True):
    print
    if isinstance(question, basestring):
        try:
            question = funcfinder.questions.functions[question]
        except KeyError:
            print "No question with name %s found" % question
            return

    sources = set()
    dependencies = set()

    _show_source_and_add_to_set(question, sources)

    if hasattr(question, "answers"):
        print "Answers:"
        print
        correct_answers = []
        for answer in question.answers:
            dependencies.update(_CodeDetector.detect(question, answer, include_questions=True))
            _show_source_and_add_to_set(answer, sources)
            try:
                question(answer)
                print "Passed tests successfully."
                print "--------------------------"
                print
                correct_answers.append(answer)
            except Exception as e:
                print "Failed tests with exception:"
                if not isinstance(e, TryImportError):
                    tb_list = traceback.extract_tb(sys.exc_info()[2])
                    tb_list = list(dropwhile(lambda entry: entry[2] != question.__name__, tb_list))
                    print "".join(traceback.format_list(tb_list)).rstrip()
                print "".join(traceback.format_exception_only(*sys.exc_info()[:2]))

        if time_answers:
            _time_answers(question, correct_answers)

        _show_dependencies(dependencies, sources)

    else:
        print "No answers have been marked as solving this question, which is a problem."
        print "The question will now be asked manually. If any solutions are found, please contribute by adding:"
        print
        print "@solves(q.%s)" % question.__name__
        print
        print "to each solution."
        print
        ask(question, time_answers=time_answers)


def _get_source(func, index_permutation=None):
    try:
        name = func.__name__
    except AttributeError:
        name = func.co_name
    pattern = r"(def\s+%s\(.+)" % name
    regex = re.compile(pattern, re.DOTALL)
    source = inspect.getsource(func).strip()
    match = regex.search(source)
    if match is not None:
        source = match.group(1)
    if index_permutation and len(index_permutation) > 1 and list(index_permutation) != sorted(index_permutation):
        pattern = r"(def\s+%s)\((.+?)\)(.+)" % name
        regex = re.compile(pattern, re.DOTALL)
        match = regex.search(source)
        if match is None:
            raise Exception("Failed to extract arguments from function definition:\n" + source)
        args = re.split(r"\s*,\s*", match.group(2), flags=re.DOTALL)
        args = _permute(args, index_permutation)
        args = ", ".join(args)
        source = "{start}({args}){rest}".format(start=match.group(1), args=args, rest=match.group(3))
    return source


def _show_source(func, source):
    print inspect.getsourcefile(func), ":", inspect.getsourcelines(func)[1]
    print source
    print


def _show_source_and_add_to_set(func, sources_set, index_permutation=None):
    source = _get_source(func, index_permutation)
    sources_set.add(source)
    _show_source(func, source)


def _time(question, answer, number=1):
    def stmt():
        question(answer)

    if number == 1:
        time_taken = 0
        while time_taken < 1:
            number *= 2
            time_taken = timeit.timeit(stmt, number=number)
    return min(timeit.repeat(stmt, number=number, repeat=5)), number


def _time_answers(question, correct_answers):
    if len(correct_answers) > 1:
        print "Best times per answer:"
        number = 1
        for answer in correct_answers:
            time_taken, number = _time(question, answer, number)
            print "%s: %.3f s" % (answer.__name__, time_taken)
        print "(among 5 sets of %i repetitions)" % number
        print


def ask(question, time_answers=True):
    num_args_holder = []

    def count_expected_args(*args):
        num_args_holder.append(len(args))

    exc_info = None

    try:
        question(count_expected_args)
    except Exception:
        exc_info = sys.exc_info()
        pass

    if not num_args_holder:
        if exc_info:
            raise exc_info[0], exc_info[1], exc_info[2]
        else:
            raise AssertionError("Failed to find the number of arguments the answer must have. "
                                 "Did you call the given function?")

    num_args = num_args_holder[0]
    index_permutations = list(permutations(range(num_args)))

    correct_answers = []
    dependencies = set()
    sources = set()
    for answer in funcfinder.answers.functions.itervalues():
        if answer.func_code.co_argcount == num_args:
            for index_permutation in index_permutations:
                try:
                    permuted_answer = _permute_args(index_permutation)(answer)
                    question(permuted_answer)
                except (_ForbiddenKwargs, _WrongNumberOfArgs) as e:
                    print e.message
                    return
                except Exception:
                    pass
                else:
                    _show_source_and_add_to_set(answer, sources, index_permutation)
                    solved_questions = getattr(answer, "solved_questions")
                    if solved_questions:
                        print "Solves the question%s %s" % (
                            "s" * (len(solved_questions) > 1),
                            ", ".join(q.__name__ for q in solved_questions))
                        print
                    print "-------------------------"
                    print
                    correct_answers.append(permuted_answer)
                    dependencies.update(_CodeDetector.detect(question, permuted_answer, include_questions=False))
                    dependencies.discard(answer.func_code)
                    break

    if not correct_answers:
        print "Sorry, no correct answers found. If you find one, please consider contributing it!"
        return

    if time_answers:
        _time_answers(question, correct_answers)
    _show_dependencies(dependencies, sources)


def _permute_args(index_permutation):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        if kwargs:
            raise _ForbiddenKwargs
        if len(index_permutation) != len(args):
            raise _WrongNumberOfArgs
        return wrapped(*_permute(args, index_permutation))

    return wrapper


def _permute(it, index_permutation):
    return (it[i] for i in index_permutation)


class _ForbiddenKwargs(Exception):
    message = "You cannot ask for a function with keyword arguments."


class _WrongNumberOfArgs(Exception):
    message = "The function you ask for must always have the same number of arguments."


class _CodeDetector(Bdb):
    def __init__(self, *args):
        Bdb.__init__(self, *args)
        self.codes = set()

    def do_clear(self, arg):
        pass

    def user_call(self, frame, argument_list):
        self.codes.add(frame.f_code)

    @classmethod
    def detect(cls, question, answer, include_questions):
        detector = cls()
        detector.set_trace()
        try:
            question(answer)
        except Exception:
            pass
        detector.set_quit()
        for func in (question, answer):
            detector.codes.discard(func.func_code)

        filtered_codes = set()

        for code in detector.codes:
            filename = code.co_filename

            def from_package(package):
                return ("funcfinder/%s/" % package) in filename and not filename.endswith("__init__.py")

            # noinspection PyTypeChecker
            if from_package("answers") or include_questions and from_package("questions"):
                filtered_codes.add(code)
        return filtered_codes
