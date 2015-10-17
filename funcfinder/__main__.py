from argparse import ArgumentParser

from funcfinder import *


def find(args):
    print "Searching for the terms %s..." % args.terms
    search_questions(args.terms)


def show(args):
    show_question(args.question, time_answers=args.time_answers)


def funcfinder_help():
    pass


def main():
    parser = ArgumentParser(
        description="Find (using docstrings, not tests) and inspect functions in the funcfinder repository.")
    subparsers = parser.add_subparsers()

    find_parser = subparsers.add_parser(
        "find",
        description="Shows questions whose docstrings contain all the given terms, ignoring case.")
    find_parser.set_defaults(func=find)
    find_parser.add_argument("terms", metavar="TERM", nargs="+")

    show_parser = subparsers.add_parser(
        "show",
        description="Shows a single question (i.e. test) and the functions that solve it.")
    show_parser.set_defaults(func=show)
    show_parser.add_argument("question",
                             help="Name of the question (typically found by first using the find subcommand).")
    show_parser.add_argument("-t", "--notime",
                             help="By default if a question has multiple solutions they are automatically timed, "
                                  "which takes a few seconds. This flag prevents that.",
                             action="store_false", dest="time_answers")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
