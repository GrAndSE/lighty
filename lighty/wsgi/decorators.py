'''Some decorators can be used to create view
'''
import functools
import operator
import sys
import traceback

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
            try:
                if args[0].app.settings.debug:
                    template = args[0].app.get_template('debug.html')
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb_list = traceback.extract_tb(exc_traceback)
                    result = template({
                        'error_type': exc_value.__class__.__name__,
                        'error_message': str(exc_value),
                        'traceback': [{'line': line, 'file': file, 
                                       'func': name, 'code': code}
                                      for file, line, name, code in tb_list]
                    })
                else:
                    result = e
            except:
                result = e
            response = http.Response(result, 500)
        return response
    return wrapper
