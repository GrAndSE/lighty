'''Some decorators can be used to create view
'''
import functools
import operator

from . import http


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
                response = http.Response('Wrong view argument value', 500)
            else:
                response = func(*args, **kwargs)
                if not isinstance(response, http.Response):
                    response = http.Response(response)
        except Exception as e:
            response = http.Response(e, 500)
        return response
    return wrapper
