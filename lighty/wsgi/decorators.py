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
    @monads.handle_exception
    def wrapper(*args, **kwargs):
        if not functools.reduce(operator.__and__, 
                                [constraints[arg](kwargs[arg])
                                 for arg in constraints]):
            return monads.NoneMonad(ValueError('Wrong view argument value'))
        return monads.ValueMonad(func(*args, **kwargs))
    return wrapper
