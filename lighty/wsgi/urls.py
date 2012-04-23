'''Package contains URL patterns management functions
'''
import copy
import re
from functools import partial, reduce

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
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


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


def escape_url(url):
    pattern = url
    for symbol in TO_ESCAPE:
        pattern = pattern.replace(symbol, '\\' + symbol)
    return pattern


def get_arg(pattern, constr):
    '''Get argument types
    '''
    actual = pattern[1:-1]
    name, type = ':' in actual and actual.split(':') or (actual, 'str')
    return (pattern, name,
            constr[name] if name in constr else TYPE_PATTERNS[type])


def replace_pattern(url, arg):
    pattern, name, regexp = arg
    return url.replace(pattern, '(?P<%s>%s)' % (name, regexp))


def replace_arg(url, arg):
    pattern, value = arg
    return url.replace(pattern, str(value))


def url(pattern, view, name='', constraints={}, methods=HTTP_METHODS,
        defaults={}):
    '''Prepare url for application
    '''
    vars = [get_arg(var, constraints)
            for var in VARIABLE_PATTERN.findall(pattern)]
    constrs = dict([(var[1], var[2]) for var in vars])
    args = dict([(var[1], var[0]) for var in vars])
    url_expr = re.compile(reduce(replace_pattern, [pattern + '$'] + vars))
    view_func = load_view(view)
    url_name = name is not '' and name or view_func
    return (url_expr, pattern, view_func, url_name, defaults, args, constrs,
            methods)


def resolve(urls, path, method=None):
    '''Resolve url
    '''
    for expr, url, view, name, defaults, _, _, methods in urls:
        if not method or method in methods:
            match = expr.match(path)
            if match:
                call_args = copy.copy(defaults)
                call_args.update(match.groupdict())
                return partial(view, **call_args)
    return NoneMonad(LookupError('There is no pattern matching path %s' %
                                 path))


def reverse(urls, lookup_name, lookup_args={}):
    '''Get url for name with specified args number
    '''
    lookup_keys = sorted(lookup_args.keys())
    for _, url, _, name, _, args, _, _ in urls:
        if name == lookup_name and lookup_keys == sorted(args.keys()):
            replacement = [(args[var], lookup_args[var])
                           for var in lookup_keys]
            return reduce(replace_arg, [url] + replacement)
    return NoneMonad(LookupError(
                            'Url for name "%s" with args "%s" was not found' %
                            (lookup_name, ','.join(lookup_keys))))
