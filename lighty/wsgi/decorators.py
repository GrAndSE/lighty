'''
'''
import functools
import operator
from .. import monads


def view(func, **constraints):
    '''Functions that decorates a view. This function can also checks the
    argument values
    '''
    func.is_view = True
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if (len(constraints) > 0 and
                    not functools.reduce(operator.__and__,
                                         [constraints[arg](kwargs[arg])
                                          for arg in constraints])):
                return monads.NoneMonad(ValueError(
                                                'Wrong view argument value'))
            return monads.ValueMonad(func(*args, **kwargs))
        except Exception as e:
            return monads.NoneMonad(e)
    return wrapper
