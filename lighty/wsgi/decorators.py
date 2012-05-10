'''Some decorators can be used to create view
'''
import functools
import operator
import sys
import traceback

from . import http


def error_page(args, exc):
    '''Build an error page
    '''
    try:
        if args[0].app.settings.debug:
            template = args[0].app.get_template('debug.html')
            _, exc_value, exc_traceback = sys.exc_info()
            tb_list = traceback.extract_tb(exc_traceback)
            tb = []
            for file_name, line, name, code in tb_list:
                start = line > 9 and line - 10 or 0
                end = start + 21
                try:
                    fh = open(file_name, 'r').readlines()[start:end]
                    lines = [{'num': n, 'code': c.rstrip(),
                              'current': n == line}
                             for n, c in enumerate(fh, start + 1)]
                except:
                    lines = []
                finally:
                    tb.append({'line': line, 'file': file_name,
                               'func': name, 'code': code,
                               'lines': lines})
            result = template({
                'error_type': exc_value.__class__.__name__,
                'error_message': str(exc_value),
                'traceback': tb
            })
        else:
            result = exc
    except:
        traceback.print_exc(file=sys.stdout)
        result = exc
    return result


def view(func, **constraints):
    '''Functions that decorates a view. This function can also checks the
    argument values
    '''
    func.is_view = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        '''Catch an exception and print pretty traceback
        '''
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
        except Exception as exc:
            response = http.Response(error_page(args, exc), 500)
        return response
    return wrapper
