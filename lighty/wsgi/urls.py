'''Package contains URL patterns management functions
'''
import re, copy

from functools import partial

PATH_PATTERN = re.compile('^(?P<module>(([\\w\\d]+\\.)*[\\w\\d]+))\\.(?P<function>([\\w\\d]+))$')

from lighty.exceptions import ApplicationException

def load_view(view):
    '''Load view for name if needed
    '''
    if callable(view):
        return view
    elif not type(view) is str:
        raise ApplicationException('Error url creation')
    explain     = PATH_PATTERN.match(view)
    if not explain:
        raise ApplicationException('%s could not be loaded' % view)
    func_name   = explain.group('function')
    pack_name   = explain.group('module')
    module      = __import__(pack_name, globals(), locals(), func_name)
    func        = getattr(module, explain.group('function'))
    if not callable(func):
        raise ApplicationException('%s.%s is not callable' % 
                                    (pack_name, func_name))
    return func

def url(pattern, view, name='', args={}):
    '''Prepare url for application
    '''
    url_expr    = re.compile(pattern)
    view_func   = load_view(view)
    url_name    = name is not '' and name or view_func
    return url_expr, pattern, view_func, url_name, args

def resolve(urls, path):
    '''Resolve url
    '''
    for expr, url, view, name, args in urls:
        match = expr.match(path)
        if match:
            call_args = copy.copy(args)
            call_args.update(match.groupdict())
            return partial(view, **call_args)
