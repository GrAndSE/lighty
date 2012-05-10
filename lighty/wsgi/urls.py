'''Package contains URL patterns management functions
'''
import copy
import functools
import re

from ..monads import NoneMonad
from . import decorators


PATH_PATTERN = re.compile(
        '^(?P<module>(([\\w\\d]+\\.)*[\\w\\d]+))\\.(?P<function>([\\w\\d]+))$')
VARIABLE_PATTERN = re.compile('(<[\w_]+[:]?[\w]{0,5}>)')
TYPE_PATTERNS = {
        'int': '[\\d]+',
        'float': '([\\d]+(\\.[\\d]*)?)',
        'char': '[\\w\\d]',
        'str': '[\\w\\d_\\-\\.\\,]+',
        'slug': '[\\w\\d_\\-]+',
        'path': '[\\w\\d_\\-\\.\\,/]+',
}
TO_ESCAPE = ('.', '\\', '[', ']', '(', ')', '+', '*', '?', '{', '}', '-', '|')
ESCAPE_SYMBOL = lambda value, symbol: value.replace(symbol, '\\' + symbol)
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'UPDATE']


def load_urls(name):
    '''Load urls file. This file requires to contains urlpatterns variable. It
    could be list or tuple of results of url() function calling.

        from app_name.views import hello_view

        urlpatterns = (
            url('/test', 'app_name.views.test_view'),
            url('/hello/(?P<name>[\w]+)', hello_view),
        )
    '''
    module = __import__(name, globals(), locals(), 'urlpatterns')
    return module.urlpatterns


def load_view(view):
    '''Load view for name if needed
    '''
    if callable(view):
        return view if hasattr(view, 'is_view') else decorators.view(view)
    elif not type(view) is str:
        return TypeError('Error url creation')
    explain = PATH_PATTERN.match(view)
    if not explain:
        return ImportError('%s could not be loaded' % view)
    func_name = explain.group('function')
    pack_name = explain.group('module')
    module = __import__(pack_name, globals(), locals(), func_name)
    func = getattr(module, explain.group('function'))
    if not callable(func):
        return TypeError('%s.%s is not callable' % (pack_name, func_name))
    return func if hasattr(func, 'is_view') else decorators.view(func)


def escape_url(value):
    '''Escape an url for regular expression
    '''
    return functools.reduce(ESCAPE_SYMBOL, [value] + TO_ESCAPE)


def get_arg(pattern, constr):
    '''Get argument types
    '''
    actual = pattern[1:-1]
    name, type_name = ':' in actual and actual.split(':') or (actual, 'str')
    return (pattern, name,
            constr[name] if name in constr else TYPE_PATTERNS[type_name])


def replace_pattern(string, (pattern, name, regexp)):
    '''Replace a pattern in string
    '''
    return string.replace(pattern, '(?P<%s>%s)' % (name, regexp))


def replace_arg(string, (pattern, value)):
    '''Replace an argument in string
    '''
    return string.replace(pattern, str(value))


def url(pattern, view, name='', **kwargs):
    '''Prepare url for application
    '''
    constraints = kwargs.get('constraints', {})
    defaults = kwargs.get('defaults', {})
    methods = kwargs.get('methods', HTTP_METHODS)
    variables = [get_arg(var, constraints)
                 for var in VARIABLE_PATTERN.findall(pattern)]
    constrs = dict([(var[1], var[2]) for var in variables])
    args = dict([(var[1], var[0]) for var in variables])
    url_expr = re.compile(functools.reduce(replace_pattern,
                                           [pattern + '$'] + variables))
    view_func = load_view(view)
    url_name = name is not '' and name or view_func
    return (url_expr, pattern, view_func, url_name, defaults, args, constrs,
            methods)


def resolve(urls, path, method=None):
    '''Resolve url for path and method name
    '''
    for expr, _, view, _, defaults, _, _, methods in urls:
        if not method or method in methods:
            match = expr.match(path)
            if match:
                call_args = copy.copy(defaults)
                call_args.update(match.groupdict())
                return functools.partial(view, **call_args)
    return NoneMonad(LookupError('There is no pattern matching path %s' %
                                 path))


def reverse(urls, lookup_name, lookup_args=None):
    '''Get url for name with specified args number
    '''
    lookup_keys = sorted(lookup_args.keys()) if lookup_args else []
    for _, pattern, _, name, _, args, _, _ in urls:
        if name == lookup_name and lookup_keys == sorted(args.keys()):
            replacement = [(args[var], lookup_args[var])
                           for var in lookup_keys]
            return functools.reduce(replace_arg, [pattern] + replacement)
    return NoneMonad(LookupError(
                            'Url for name "%s" with args "%s" was not found' %
                            (lookup_name, ','.join(lookup_keys))))
