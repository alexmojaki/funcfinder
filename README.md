# funcfinder

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/alexmojaki/funcfinder?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

funcfinder is a new way to solve problems of the form "I need a Python function that does X". This is commonly solved using search engines and forums where the results exist in the form of mere text. Some of it may represent code, but it can't be executed. funcfinder is a repository of 'questions', which are parametrised unit tests, and 'answers', which are functions that satisfy the tests. By using actual code, new possibilities open up:

* Answers to questions are essentially guaranteed to be correct because they are unit tested.
* Questions can have multiple answers, meaning the same unit test is applied to different functions, which has several implications:
    * Unit testing code is effectively reused.
    * Every answer is timed automatically to show performance differences.
    * You can 'try out' multiple answers simultaneously by passing sample input to them all and seeing how the results subtly differ.
    * You can easily switch between answers with reduced risk of breaking your code, e.g. if:
        * It turns out an answer has a bug.
        * Someones creates a new answer which is more efficient.
        * You find you have more specific requirements, e.g. you need a function that handles any iterable, not just lists.
* New questions can be asked using only code by giving a simple test with a sample of what the function should do. For example, `assert func(["a", "bb", "c"], len) == {1: ["a", "c"], 2: ["bb"]}` describes a function which groups elements of an iterable into a dictionary based on some key function. This little test is run against the entire repository of functions to find an answer automatically.
* Questions can depend on other questions through simple function calls (more code reuse!) which are detected automatically. Since this is expressed in code, various complex relationships are possible, but the most common case is an inheritance hierarchy of requirements for answers to satisfy. This lets you easily navigate from functions with loose requirements to functions with more specific ones.
* Answers can also use each other and again this can be detected automatically. The result is that:
    * Answers to complex questions are easier to write because a whole repository of generically useful functions is available.
    * Answers are cleanly divided into small functions with different levels of abstraction, resulting in more readable code.
    * In the process of finding a function to solve one specific problem you can find more generic functions which you are likely to use elsewhere.
* By not relying on natural language descriptions:
    * There is no doubt or ambiguity in what is being asked for, or what the answer accomplishes.
    * There is no need to know a particular language (e.g. English) to ask a question, answer it, or to understand both the question and answer.
    
This repository is a basic implementation of this idea providing the most essential features. It's an experiment to see if people are interested and willing to contribute questions and answers. If so, it may be turned into a complete website, which could ultimately mean answers appearing directly in Google searches. Imagine having all of the above, with no installation effort, a fancy frontend, maybe even integration with Stack Overflow. Imagine having implementations for other languages. If this excites you, read on.

## Table of Contents

* [Getting started](#getting-started)
* [Usage](#usage)
  * [Searching](#searching)
  * [Showing questions](#showing-questions)
    * [The question](#the-question)
    * [Answers](#answers)
    * [Dependencies](#dependencies)
  * [Asking questions](#asking-questions)
* [Contributing](#contributing)
  * [Folder structure](#folder-structure)
  * [Naming](#naming)
  * [Imports](#imports)
  * [Writing questions](#writing-questions)
  * [Writing answers](#writing-answers)
    * [Answers ignored when asking](#answers-ignored-when-asking)
* [FAQ](#faq)

## Getting started

Fork this repository, clone your fork, then run

`python setup.py develop`

within the main directory. This will install the library so that you can use it in Python scripts anywhere, and also ensure that changes in the repository (whether you make them or you pull in remote updates) are immediately reflected in scripts. It also installs the shell command `funcfinder`.

## Usage

### Searching

Finding a function typically begins with a simple keyword search. The `funcfinder` shell command is made for this. By itself, or with the flag `-h`, it will give you some help on usage in case you get lost. To search for a function, use the `find` subcommand. This takes any number of positional arguments representing search terms. The results are questions (answers come later) whose docstrings contain all the search terms directly, ignoring case. You can use quotes to force terms to appear together.

For example, let's say we want a dictionary where the keys are in sorted order. This might go like this:

```
$ funcfinder find dict sort
Searching for the terms ['dict', 'sort']...

sort_dict_by_key:

Return a copy of a dict which still supports all the standard operations with the usual API,
plus can be iterated over in sorted order by key. Adding keys to the dict may not necessarily preserve this order -
for that, see always_sorted_dict_by_key.

-----------------------

sort_dict_by_value:

Return a copy of a dict which still supports all the standard operations with the usual API,
plus can be iterated over in sorted order by value. Adding keys to the dict may not necessarily preserve this order.

-----------------------

always_sorted_dict_by_key:

Return a copied dict sorted by key which preserves its order upon updates.

-----------------------
```

Here we see the names and docstrings of all the questions that satisfied the search.

### Showing questions

Suppose that `sort_dict_by_key` sounds most like what we want. We can take a closer look using the `show` subcommand. An example is below. This looks like a lot to absorb, but most of it is source code for the various pieces involved, along with where to find it. This is great for when you actually use the tool, but understanding it all is not required for this tutorial. We'll walk through it.

```
$ funcfinder show sort_dict_by_key

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/questions/dict.py : 51
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

Answers:

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/dict.py : 14
def ordered_dict_sorted_by_key(d):
    return collections.OrderedDict(sorted(d.items()))

Passed tests successfully.
--------------------------

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/dict.py : 19
def sorted_dict(d):
    return sortedcontainers.SortedDict(d)

Failed tests with exception:
TryImportError: No module named sortedcontainers

Dependencies:

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/questions/dict.py : 22
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
```

#### The question

The first thing in the output is the source code of the question. A question is a function which takes a single argument, also a function, traditionally named `func`. `func` is a potential answer to the question: the question will call it with whatever arguments it wants and make assertions about the results. `func` is considered a correct solution if the whole question can execute without any errors. So a question is just a unit test that tests a single function. By reading it you can be confident about what the answer(s) will provide.

#### Answers

Next we see answers to the question that have been marked as solutions. These are immediately tested against the question to make sure they work. Indeed, the second of the two answers failed with an exception! Normally we would see a traceback, but this is a special case: a `TryImportError` just indicates that you're missing some required library to use this answer. Questions and answers can freely use any third party libraries and nothing will go wrong if you don't have them installed. They just have to be imported slightly differently.

[sortedcontainers](http://www.grantjenks.com/docs/sortedcontainers/) is a potentially useful library and can easily be installed using `pip`. Suppose we install it. Now the answer passes the tests defined by the question, and we also get something extra:

```
...

Answers:

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/dict.py : 14
def ordered_dict_sorted_by_key(d):
    return collections.OrderedDict(sorted(d.items()))

Passed tests successfully.
--------------------------

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/dict.py : 19
def sorted_dict(d):
    return sortedcontainers.SortedDict(d)

Passed tests successfully.
--------------------------

Best times per answer:
ordered_dict_sorted_by_key: 1.692 s
sorted_dict: 0.587 s
(among 5 sets of 64 repetitions)

...
```

Whenever a question has more than one correct answer, they are automatically timed. Now we can see that sortedcontainers is significantly faster than the standard library solution.

#### Dependencies

The last part of the output shows dependencies, which are other questions or answers that were called when running the test. This means that questions and answers can be reused by authors freely, while users still get to see all the relevant source code.

In this case the `sort_dict_by_key` question directly tests properties related to order, but it also has the requirement that the dictionary it returns is a new, separate copy of the original. This requirement is expressed in the first line with the statement `copy_dict(func)`. This does not mean that a dictionary `func` is being copied, but that the answer `func` must also solve the question `copy_dict`. `copy_dict` itself is not a difficult question - the method `dict.copy()` can solve that - but it is a common requirement for other questions. `sort_dict_by_value` is an example of another question that reuses `copy_dict`.

The function call `copy_dict(func)` is all that is needed from the question author. funcfinder picks it up automatically and prints the source of `copy_dict` at the end so that users can immediately see the additional requirements imposed by the `sort_dict_by_key` question. The same goes for answers. For example, the `is_even` answer shown in the next section uses the `is_divisible_by` answer, so that is printed out as well.

### Asking questions

If you can't find a question by searching normally then it's time to write a question in code. Here's a simple example:

```
import funcfinder

def how_to_check_if_number_is_even(func):
    assert func(2)
    assert not func(3)
    assert func(4)

funcfinder.ask(how_to_check_if_number_is_even)
```

If you're still confused about what a question is, read [here](#the-question). The output of running this script is (roughly):

```
/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/math.py : 11
def is_even(a):
    return is_divisible_by(a, 2)

Solves the question is_even

-------------------------

Dependencies:

/Users/alexhall/Dropbox/python/funcfinder/funcfinder/answers/math.py : 6
def is_divisible_by(a, b):
    return a % b == 0
```

Note that the question does not need to thoroughly test the function. Just give enough detail to narrow things down. Most answers in the repository won't even expect an integer as input and will fail immediately. A few unwanted answers could potentially survive this test (e.g. check if the number is a power of two), but it's very easy to either take a quick look and see which answer you actually need, or to add a couple more test cases to narrow things down (e.g. `assert func(6)`).

If answers are found they will come with names of questions that they solve, which you can inspect with `funcfinder show` to see more detailed tests.

There are just a few simple guidelines to asking questions:

Every call to `func` in the question must have the same number of arguments, none of them named. You're looking for a solution to a specific problem, not a neat API.

Keep in mind that your question is going to run a large number of times. Keep the inputs small: small numbers, short lists, etc. Definitely don't pass any infinite iterators. Call the given function as soon as possible so that it can fail quickly for wrong answers. If your question involves something even slightly slow such as setting up a database connection or opening a file, try to do it once outside the question definition. This is safe as answers are not allowed to modify these resources (see below), but you should still reset iterators and database cursors and seek to the beginning of files at the start of the question.

Some answers will be marked to say that they should be ignored by `funcfinder.ask`; read more [here](#answers-ignored-when-asking) so that you don't waste your time.

If the output of your function should be some kind of iterable (e.g. a list or a tuple) and you're not 100% sure what the type will be, consider the functions `assertEqualIters` and `assertDeepEqualIters` from the `funcfinder.utils` module.

There's one last catch when it comes to asking (and searching for) questions. You probably won't find any answers, because the repo is brand new and contains very few questions and answers. If you find the idea of this repo exciting, if you want it to succeed, it's going to need your help.

## Contributing

It will take a large community effort to make this repo useful. So the first thing you can do to help is recruit others. Tell your friends and coworkers. Talk about funcfinder in programming forums. Write a blog post. Anything that will multiply your impact.

If you have concerns or suggestions, feel free to open an issue, join the discussion on an existing one, or [come chat on gitter](https://gitter.im/alexmojaki/funcfinder?utm_source=share-link&utm_medium=link&utm_campaign=share-link). All feedback is welcome.
 
If you're willing to write some questions and answers, excellent! You can contribute any functions that you think someone else is likely to look for. This might be the case if you:

* Tried to find it here yourself and couldn't.
* Saw someone else looking for such a function online.
* Have functions in your own code that are generic enough that someone else might want to solve the same problem, especially if *you* are likely to use them again in a different project.

Be aware that any code contributions fall under the MIT License and anyone else can use the code however they please.

Writing questions and answers is pretty simple and straightforward, but there are some rules and guidelines that you need to know.

### Folder structure

Questions are placed in modules in the `funcfinder.questions` package. The modules can have any name (other than `__init__`, don't touch those) and can be organised further into nested packages as desired. The aim of this is simply to avoid a single monolithic file of questions. The names of modules have no real semantics, just try to pick a sensible module for each question. The structure of the package `funcfinder.answers` must match `funcfinder.questions` exactly.

### Naming

All questions must be uniquely named, and all answers must be uniquely named, even across packages. A question and an answer can have the same name. `funcfinder show` can be used to easily check if a question name is taken. If there is a naming conflict it should throw an error at runtime, unless the name was defined twice in the same file.

### Imports

All modules must contain the following imports:

```
from __future__ import absolute_import
from funcfinder.utils import *
```

An answers module must also import the corresponding questions module with the alias `q`, i.e.
```import funcfinder.questions.x.y.z as q```

Imports from the standard library should appear at the top as `import module_name`. The forms `import x as y` and `from x import y` are forbidden.

Imports from within `funcfinder` itself must also be fully qualified, with no alias. You can create an alias inside the answer using assignment, e.g.
```useful_function = funcfinder.answers.module.useful_function```

Other libraries should be imported using the `try_import` function already imported from `funcfinder.utils`, e.g.

```sortedcontainers = try_import("sortedcontainers")```

The names on the left and right must match. Using this will prevent errors for users who don't have the library installed, but the `ImportError` will still be raised (wrapped in a `TryImportError`) if you try to use the module. This is how the answer `sorted_dict` raised a `TryImportError` in the tests in the example above even though there was no visible import. It also means that IDEs and other tools won't complain about modules that can't be found.

### Writing questions

Questions should:

* Have at least one answer. If you think leaving unsolved questions should be allowed, share your thoughts [here](https://github.com/alexmojaki/funcfinder/issues/1).
* Include a docstring explaining exactly what the answer function must accomplish. Be as clear as possible and include plenty of detail. Insert synonyms for words so that the question is more likely to be found. Remember that searching for questions is [(for now)](https://github.com/alexmojaki/funcfinder/issues/2) more like using `grep` than Google.
* Use the `assert*` functions from `funcfinder.utils` instead of raw `assert` statements.
* Use `assertEqualIters` and `assertDeepEqualIters` where the flexibility is needed.
* Have little performance overhead relative to their solutions so that timing them shows the difference clearly, although clarity should be preferred over minor optimisations.
* Be thorough, like real unit tests.
* Have a single parameter named `func`.
* Always call `func` with the same number of arguments, and not use keyword arguments.
* Call to a common 'base' question where appropriate instead of repeating tests.

### Writing answers

A solution to a question must be in the module corresponding to the question, i.e. an answer under `funcfinder.answers.x.y.z` must solve a question in `funcfinder.questions.x.y.z`. The exception is if an answer solves questions in multiple modules, but this probably indicates poor question placement.

All answers must have the `solves` decorator (which has been imported from `funcfinder.utils`), with the solved questions as arguments. For example:

```
@solves(q.sort_dict_by_key, q.always_sorted_dict_by_key)
def sorted_dict(d):
    ...
```

An answer doesn't *have* to be marked as solving a question even if it does. For example the answer `sorted_dict` above also solves the question `copy_dict` because `copy_dict` is a requirement of the question `sort_dict_by_key`, but someone who just wants to know how to copy a dictionary doesn't need to know how to sort it. This doesn't mean that there cannot be any 'redundancy' in the `solves` decorator: for example, the question `sort_dict_by_key` is a requirement of the question `always_sorted_dict_by_key` so it might seem that the decorator is stating more than necessary. However by doing this, the answer will show up when someone takes a look at either of the two questions.

Answers should also:

* Use `@ask_ignore` when appropriate; [see below](#answers-ignored-when-asking).
* Have a plain signature: no `*args`, `**kwargs`, `arg=default`, or tuple unpacking.
* Use other answers where appropriate.
* Not use libraries whose source isn't easily available and which are neither somewhat popular (e.g. at least 20 stars on GitHub) nor very small. In other words, it should be easy to verify that the library is trustworthy. Good documentation is also important in this regard.
* Never enter an infinite loop unless the input is an infinite iterator. Don't count the iterations of a loop and break when the count is too high, but handle unexpected finite input. For example, the following is unacceptable because it will never terminate if `b` is `-1` or `0.5`:
  
```
def pow(a, b):
    """Returns a^b, where b is a positive integer."""
    result = 1
    while b != 0:
        result *= a
        b -= 1
    return result
```

Once you've finished answering a question, run the `funcfinder show` command to make sure it works. If you see that the question has multiple solutions, and one might be significantly faster than another, consider ensuring that the question is able to demonstrate the performance difference. This means adding one or more test cases at the end of the question that have a medium sized input, if none are present. If you do this, remember to run `funcfinder show` again at the end. Don't change the question if one of the answers requires a library that you don't have and aren't willing to install - you don't want to unknowingly break an answer. By the way, the `-t` flag will prevent `funcfinder` from timing answers, just in case that starts to annoy you.

#### Answers ignored when asking

There are some kinds of answers that are worth having in the repository for people to find by searching but create problems for users of `funcfinder.ask`. You should use the decorator `@ask_ignore` when you write such a problematic answer. `funcfinder.ask` will then skip over the answer when looking for a solution to a question.

There are two common cases to use this decorator. The first is if the function is likely to cause a test to take a significant amount of time, even when given 'small' inputs of a common type. Examples include the [Ackermann function](https://en.wikipedia.org/wiki/Ackermann_function) or functions which connect to the Internet. The second case is answers which mutate or modify external resources such as files or databases, or anything else that takes time to set up in a clean state. This includes calling `.close()` or a similar method on anything. This way users can set up these resources for testing outside of a question, speeding up the asking process, and not worry about answers interfering with each other in the test.

## FAQ

**What if I ask a question and my test always throws an exception because I made a mistake?**
If the exception is thrown before any calls to `func` are made, it'll be picked up and shown to you. Otherwise funcfinder will fail to find an answer, just as if there really wasn't one.

**What if I ask a question looking for a function with multiple arguments?**
No problem. funcfinder will automatically try out every possible rearrangement behind the scenes. It will even rearrange the arguments in the source code it prints for you to match your question. In short, this is not an issue.
