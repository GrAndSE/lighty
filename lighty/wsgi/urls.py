'''Package contains URL patterns management functions
'''
import copy
import re
from functools import partial

from lighty.exceptions import ApplicationException, NotFoundException


PATH_PATTERN = re.compile(
        '^(?P<module>(([\\w\\d]+\\.)*[\\w\\d]+))\\.(?P<function>([\\w\\d]+))$')
VARIABLE_PATTERN = re.compile('(<[\w_]+[:]?[\w]{0,5}>)')
TYPE_PATTERNS = {
        'int': '[\\d]+',
        'str': '[\\w\\d_\\-\\.\\,]+',
        'char': '[\\w\\d]',
        'float': '([\\d]+(\\.[\\d]*)?)',
}
TO_ESCAPE = ('.', '\\', '[', ']', '(', ')', '+', '*', '?', '{', '}', '-', '|')
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


def load_view(view):
    '''Load view for name if needed
    '''
    if callable(view):
        return view
    elif not type(view) is str:
        return ApplicationException('Error url creation')
    explain = PATH_PATTERN.match(view)
    if not explain:
        return ApplicationException('%s could not be loaded' % view)
    func_name = explain.group('function')
    pack_name = explain.group('module')
    module = __import__(pack_name, globals(), locals(), func_name)
    func = getattr(module, explain.group('function'))
    if not callable(func):
        return ApplicationException('%s.%s is not callable' %
                                    (pack_name, func_name))
    return func


def escape_url(url):
    pattern = url
    for symbol in TO_ESCAPE:
        pattern = pattern.replace(symbol, '\\' + symbol)
    return pattern


def make_pattern(url, constr):
    def replace_pattern(url, pattern):
        actual = pattern[1:-1]
        name, type = ':' in actual and actual.split(':') or (actual, 'str')
        regexp = name in constr and constr[name] or TYPE_PATTERNS[type]
        return url.replace(pattern, '(?P<%s>%s)' % (name, regexp))
    return reduce(replace_pattern,
                  [url + '$'] + VARIABLE_PATTERN.findall(url))


def url(pattern, view, name='', args={}, constraints={}, methods=HTTP_METHODS):
    '''Prepare url for application
    '''
    url_expr = re.compile(make_pattern(pattern, constraints))
    view_func = load_view(view)
    url_name = name is not '' and name or view_func
    return url_expr, pattern, view_func, url_name, args, constraints, methods


def resolve(urls, path, method=None):
    '''Resolve url
    '''
    for expr, url, view, name, args, _, methods in urls:
        if method in methods:
            match = expr.match(path)
            if match:
                call_args = copy.copy(args)
                call_args.update(match.groupdict())
                return partial(view, **call_args)
    return NotFoundException('There is no pattern matching path %s' % path)


def reverse(urls, lookup_name, lookup_args={}):
    '''Get url for name with specified args number
    '''
    lookup_keys = sorted(lookup_args.keys())
    for _, url, _, name, args in urls:
        if name == lookup_name and lookup_keys == sorted(args.keys()):
            return url
    return NotFoundException('Url for name "%s" with args "%s" was not found' %
                             (lookup_name, ','.join(lookup_keys)))
