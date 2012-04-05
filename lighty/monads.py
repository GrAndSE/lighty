'''Monaidic functions and classes
'''
import functools
import operator


def monad_operation(func):
    '''Wrap method with exception catching and creating NoneMonad if there was
    an exception
    '''
    @functools.wraps(func)
    def wrapper(self):
        try:
            return ValueMonad(func(self))
        except Exception as e:
            return NoneMonad(e)
    return wrapper


def monad_operator(func):
    '''Decorator that wraps function with one arugment type checking and 
    exception catching
    '''
    @functools.wraps(func)
    def wrapper(self, value):
        try:
            print func, self, value
            if isinstance(value, NoneMonad):
                return value
            else:
                return ValueMonad(func(self, value.value
                                       if isinstance(value, ValueMonad)
                                       else value))
        except Exception as e:
            return NoneMonad(e)
    return wrapper


def check_argument(arg):
    '''Function that checks an argument and raises exception stored in
    argument
    '''
    if isinstance(arg, NoneMonad):
        raise arg.value
    else:
        return arg.value if isinstance(arg, ValueMonad) else arg


def monad_function(func):
    '''Decorator that wraps function with arguments, check all the values and 
    catch all the exceptions
    '''
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            nargs = [check_argument(args) for args in args]
            nkwargs = dict([(name, check_argument(kwargs[name]))
                            for name in kwargs])
            return ValueMonad(func(self, *nargs, **nkwargs))
        except Exception as e:
            return NoneMonad(e)
    return wrapper


@functools.total_ordering
class ValueMonad(object):
    '''Base monad class
    '''
    __slots__ = ('__init__', '__lt__', '__gt__', '__le__', '__ge__', '__eq__',
                 '__ne__', '__add__', '__sub__', '__div__', '__mul__',
                 '__mod__', '__pow__', '__getitem__', '__delitem__',
                 '__setitem__', '__iter__', '__contains__', '__len__',
                 '__and__', '__or__', '__xor__', '__lshift__', '__rshift__',
                 '__call__', '__str__', '__getattr__', 'code', 'value', )

    def __init__(self, value, code=200):
        super(ValueMonad, self).__init__()
        self.value = value
        self.code = 200

    @monad_operator
    def __lt__(self, other):
        return self.value < other

    @monad_operator
    def __eq__(self, other):
        return self.value == other

    @monad_operator
    def __add__(self, other):
        return self.value + other

    @monad_operator
    def __sub__(self, other):
        return self.value - other

    @monad_operator
    def __div__(self, other):
        return self.value / other

    @monad_operator
    def __mul__(self, other):
        return self.value * other

    @monad_operator
    def __mod__(self, other):
        return self.value // other

    @monad_operator
    def __pow__(self, other):
        return self.value ** other

    @monad_operator
    def __and__(self, other):
        return self.value & other

    @monad_operator
    def __or__(self, other):
        return self.value | other

    @monad_operator
    def __xor__(self, other):
        return self.value % other

    @monad_operator
    def __lshift__(self, other):
        return self.value << other

    @monad_operator
    def __rshift__(self, other):
        return self.value >> other

    def __len__(self):
        try:
            return len(self.value)
        except:
            return 1

    @monad_operator
    def __contains__(self, item):
        return item in self.value

    @monad_function
    def __iter__(self):
        return self.value.iter()

    @monad_function
    def __getitem__(self, *args):
        return operator.getitem(*args)

    @monad_function
    def __delitem__(self, *args):
        return operator.delitem(*args)

    @monad_function
    def __setitem__(self, *args):
        return operator.setitem(*args)

    @monad_function
    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    @monad_operator
    def __getattr__(self, name):
        return getattr(self.value, name)

    def __str__(self):
        return str(self.value)


class NoneMonad(ValueMonad):
    '''NoneMonad class represents all the methods exceptions and missed values
    '''
    pass
