'''Monaidic functions and classes
'''
import functools
import itertools
import operator
import sys

from . import functor, utils


def handle_exception(func):
    '''Handle an exception and return ErrorMonad for this exception
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        '''Catch an exception an return ErrorMonad for it
        '''
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            _, _, exc_traceback = sys.exc_info()
            return ErrorMonad(exc, traceback=exc_traceback)
    return wrapper


def monad_operation(func):
    '''Wrap method with exception catching and creating ErrorMonad if there was
    an exception
    '''
    return functools.wraps(handle_exception(lambda self:
                                            ValueMonad(func(self))), func)


def monad_operator(func):
    '''Decorator that wraps function with one arugment type checking and
    exception catching
    '''
    @functools.wraps(func)
    @handle_exception
    def wrapper(self, value):
        '''Check an argument type
        '''
        if isinstance(value, NoneMonad):
            return value
        return ValueMonad(func(self, value.value
                                     if isinstance(value, ValueMonad)
                                     else value))
    return wrapper


def monad_boolean(func):
    '''Decorator wraps all methods can be used for comparision.
    Return's True if boolean operation returns True, or False when boolean
    operation return's False or something goes wrong
    '''
    @functools.wraps(func)
    def wrapper(self, value):
        try:
            if isinstance(value, NoneMonad):
                return False
            else:
                return func(self, value.value if isinstance(value, ValueMonad)
                                  else value)
        except Exception:
            return False
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
    @handle_exception
    def wrapper(self, *args, **kwargs):
        nargs = [check_argument(args) for args in args]
        nkwargs = dict([(name, check_argument(kwargs[name]))
                        for name in kwargs])
        return ValueMonad(func(self, *nargs, **nkwargs))
    return wrapper

BOOLEAN_OPERATORS = set((operator.__lt__, operator.__le__, operator.__eq__,
                         operator.__ge__, operator.__gt__, ))


def __getattr__(self, name):
    return getattr(self.value, name)


class ValueMonad(functor.BaseFunctor):
    '''Base monad class. All the operations except comparisions and few others
    returns monads.
    '''
    __slots__ = ('__init__', '__getitem__', '__delitem__', '__setitem__',
                 '__iter__', '__len__', '__call__', '__str__', 'value', )
    _lazy = (operator.__lt__, operator.__le__, operator.__eq__,
             operator.__ge__, operator.__gt__, operator.__add__,
             operator.__sub__, operator.__mod__, operator.__pow__,
             operator.__mul__, operator.__contains__, __getattr__,
             operator.__rshift__, operator.__lshift__, operator.__and__,
             operator.__or__, operator.__xor__) + utils.div_operators

    def __init__(self, value):
        '''Create new monad including value
        '''
        super(ValueMonad, self).__init__()
        self.value = value.value if isinstance(value, ValueMonad) else value

    def create_copy(self, operator, operand):
        is_boolean = operator in BOOLEAN_OPERATORS
        if isinstance(operand, NoneMonad):
            return False if is_boolean else operand
        value = operator.value if isinstance(operand, ValueMonad) else operand
        try:
            result = operator(self.value, value)
        except Exception as e:
            return False if is_boolean else ErrorMonad(e)
        else:
            return result if is_boolean else ValueMonad(result)

    def __len__(self):
        try:
            length = len(self)
        except:
            return 1
        else:
            return length

    @monad_function
    def __iter__(self):
        return self.value.iter()

    @monad_function
    def __getitem__(self, *args):
        try:
            return operator.getitem(self.value, *args)
        except Exception as e:
            if len(args) == 1 and args[0] == 0:
                return self.value
            raise e

    @monad_function
    def __delitem__(self, *args):
        return operator.delitem(self.value, *args)

    @monad_function
    def __setitem__(self, *args):
        return operator.setitem(self.value, *args)

    @monad_function
    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __str__(self):
        return str(self.value)

    def __index__(self):
        return self.value if hasattr(self.value, '__index__') else None


class NoneMonad(ValueMonad):
    '''NoneMonad class represents empty list, dicts, NoneType or False
    '''
    EMPTY_ITER = itertools.cycle('')

    def __init__(self, value):
        '''Create new monad including value and store the code
        '''
        super(NoneMonad, self).__init__(value)

    def __len__(self):
        '''Returns 0
        '''
        return 0

    def __iter__(self):
        '''Return's empty iterator
        '''
        return ValueMonad(NoneMonad.EMPTY_ITER)

    def __index__(self):
        '''None as index
        '''
        return None

    def __nonzero__(self):
        '''NoneMonad equals zero
        '''
        return False


class ErrorMonad(NoneMonad):
    '''ErrorMonad class represents errors
    '''

    def __init__(self, value, traceback=None):
        '''Include traceback representation
        '''
        super(ErrorMonad, self).__init__(value)
        self.traceback = traceback
