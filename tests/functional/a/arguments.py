# pylint: disable=too-few-public-methods, missing-docstring,import-error,wrong-import-position
# pylint: disable=wrong-import-order, unnecessary-lambda, consider-using-f-string
# pylint: disable=unnecessary-lambda-assignment, no-self-argument, unused-argument, kwarg-superseded-by-positional-arg

def decorator(fun):
    """Decorator"""
    return fun


class DemoClass:
    """Test class for method invocations."""

    @staticmethod
    def static_method(arg):
        """static method."""
        return arg + arg

    @classmethod
    def class_method(cls, arg):
        """class method"""
        return arg + arg

    def method(self, arg):
        """method."""
        return (self, arg)

    @decorator
    def decorated_method(self, arg):
        """decorated method."""
        return (self, arg)


def function_1_arg(first_argument):
    """one argument function"""
    return first_argument

def function_3_args(first_argument, second_argument, third_argument):
    """three arguments function"""
    return first_argument, second_argument, third_argument

def function_default_arg(one=1, two=2):
    """function with default value"""
    return two, one


function_1_arg(420)
function_1_arg()  # [no-value-for-parameter]
function_1_arg(1337, 347)  # [too-many-function-args]

function_3_args(420, 789)  # [no-value-for-parameter]
# +1:[no-value-for-parameter,no-value-for-parameter,no-value-for-parameter]
function_3_args()
function_3_args(1337, 347, 456)
function_3_args('bab', 'bebe', None, 5.6)  # [too-many-function-args]

function_default_arg(1, two=5)
function_default_arg(two=5)

function_1_arg(bob=4)  # [unexpected-keyword-arg,no-value-for-parameter]
function_default_arg(1, 4, coin="hello")  # [unexpected-keyword-arg]

function_default_arg(1, one=5)  # [redundant-keyword-arg]

# Remaining tests are for coverage of correct names in messages.
my_lambda = lambda arg: 1

my_lambda()  # [no-value-for-parameter]

def method_tests():
    """Method invocations."""
    demo = DemoClass()
    demo.static_method()  # [no-value-for-parameter]
    DemoClass.static_method()  # [no-value-for-parameter]

    demo.class_method()  # [no-value-for-parameter]
    DemoClass.class_method()  # [no-value-for-parameter]

    demo.method()  # [no-value-for-parameter]
    DemoClass.method(demo)  # [no-value-for-parameter]

    demo.decorated_method()  # [no-value-for-parameter]
    DemoClass.decorated_method(demo)  # [no-value-for-parameter]

# Test a regression (issue #234)
import sys

class Text:
    """ Regression """

    if sys.version_info > (3,):
        def __new__(cls):
            """ empty """
            return object.__new__(cls)
    else:
        def __new__(cls):
            """ empty """
            return object.__new__(cls)

Text()

class TestStaticMethod:

    @staticmethod
    def test(first, second=None, **kwargs):
        return first, second, kwargs

    def func(self):
        self.test(42)
        self.test(42, second=34)
        self.test(42, 42)
        self.test() # [no-value-for-parameter]
        self.test(42, 42, 42) # [too-many-function-args]


class TypeCheckConstructor:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def test(self):
        type(self)(1, 2, 3) # [too-many-function-args]
        # +1: [no-value-for-parameter,no-value-for-parameter]
        type(self)()
        type(self)(1, lala=2) # [no-value-for-parameter,unexpected-keyword-arg]
        type(self)(1, 2)
        type(self)(first=1, second=2)


class Test:
    """ lambda needs Test instance as first argument """
    lam = lambda self, icon: (self, icon)

    def test(self):
        self.lam(42)
        self.lam() # [no-value-for-parameter]
        self.lam(1, 2, 3) # [too-many-function-args]

Test().lam() # [no-value-for-parameter]

# Don't emit a redundant-keyword-arg for this example,
# it's perfectly valid

class Issue642:
    attr = 0
    def __str__(self):
        return "{self.attr}".format(self=self)

# These should not emit anything regarding the number of arguments,
# since they have something invalid.
from ala_bala_portocola import unknown

# pylint: disable=not-a-mapping,not-an-iterable

function_1_arg(*unknown)
function_1_arg(1, *2)
function_1_arg(1, 2, 3, **unknown)
function_1_arg(4, 5, **1)
function_1_arg(5, 6, **{unknown: 1})
function_1_arg(**{object: 1})
function_1_arg(**{1: 2})

def no_context_but_redefined(*args):
    args = [1]
    #+1: [no-value-for-parameter, no-value-for-parameter]
    expect_three(*list(args))

def no_context_one_elem(*args):
    expect_three(args) # [no-value-for-parameter, no-value-for-parameter]

# Don't emit no-value-for-parameter for this, since we
# don't have the context at our disposal.
def expect_three(one, two, three):
    return one + two + three


def no_context(*args):
    expect_three(*args)

def no_context_two(*args):
    expect_three(*list(args))

def no_context_three(*args):
    expect_three(*set(args))

def compare_prices(arg):
    return set((arg, ))

def find_problems2(prob_dates):
    for fff in range(10):
        prob_dates |= compare_prices(fff)


from collections import namedtuple


def namedtuple_replace_issue_1036():
    cls = namedtuple('cls', 'a b c')
    new_instance = cls(1, 2, 3)._replace(
        a=24,
        b=24,
        c=42
    )
    # +1:[unexpected-keyword-arg,unexpected-keyword-arg]
    new_bad_instance = cls(1, 2, 3)._replace(d=24, e=32)
    return new_instance, new_bad_instance


from functools import partial

def some_func(first, second, third):
    return first + second + third


partial(some_func, 1, 2)(3)
partial(some_func, third=1, second=2)(3)
partial(some_func, 1, third=2)(second=3)
partial(some_func, 1)(1)  # [no-value-for-parameter]
partial(some_func, 1)(third=1)  # [no-value-for-parameter]
partial(some_func, 1, 2)(third=1, fourth=4)  # [unexpected-keyword-arg]


def mutation_decorator(fun):
    """Decorator that changes a function's signature."""
    def wrapper(*args, do_something=True, **kwargs):
        if do_something:
            return fun(*args, **kwargs)

        return None

    return wrapper


def other_mutation_decorator(fun):
    """Another decorator that changes a function's signature"""
    def wrapper(*args, do_something=True, **kwargs):
        if do_something:
            return fun(*args, **kwargs)

        return None

    return wrapper


@mutation_decorator
def mutated_function(arg):
    return arg


@other_mutation_decorator
def mutated(arg):
    return arg


mutated_function(do_something=False)
mutated_function()

mutated(do_something=True)


def func(one, two, three):
    return one + two + three


call = lambda *args: func(*args)


# Ensure `too-many-function-args` is not emitted when a function call is assigned
# to a class attribute inside the class where the function is defined.
# Reference: https://github.com/pylint-dev/pylint/issues/6592
class FruitPicker:
    def _pick_fruit(fruit):
        def _print_selection(self):
            print(f"Selected: {fruit}!")
        return _print_selection

    pick_apple = _pick_fruit("apple")
    pick_pear = _pick_fruit("pear")

picker = FruitPicker()
picker.pick_apple()
picker.pick_pear()


def name1(apple, /, **kwargs):
    """
    Positional-only parameter with `**kwargs`.
    Calling this function with the `apple` keyword should not emit
    `redundant-keyword-arg` since it is added to `**kwargs`.

    >>> name1("Red apple", apple="Green apple")
    "Red apple"
    {"apple": "Green apple"}
    """
    print(apple)
    print(kwargs)


name1("Red apple", apple="Green apple")


def name2(apple, /, banana, **kwargs):
    """
    Positional-only parameter with positional-or-keyword parameter and `**kwargs`.
    """


# `banana` is redundant
# +1:[redundant-keyword-arg]
name2("Red apple", "Yellow banana", apple="Green apple", banana="Green banana")


# Test `no-value-for-parameter` in the context of positional-only parameters

def name3(param1, /, **kwargs): ...
def name4(param1, /, param2, **kwargs): ...
def name5(param1=True, /, **kwargs): ...
def name6(param1, **kwargs): ...

name3(param1=43)  # [no-value-for-parameter]
name3(43)
name4(1, param2=False)
name5()
name6(param1=43)


# https://github.com/pylint-dev/pylint/issues/9036
# No value for argument 'string' in staticmethod call (no-value-for-parameter)
class Foo:
    @staticmethod
    def func(string):
        return string

    func(42)
    a = func(42)

isinstance(1) # [no-value-for-parameter]
