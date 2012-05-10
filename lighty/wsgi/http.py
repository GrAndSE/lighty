'''Module contains methods to work with request and response objects
'''
import collections
try:
    import Cookie
    SimpleCookie = Cookie.SimpleCookie
except:
    from http import cookies
    SimpleCookie = cookies.SimpleCookie
try:
    import httplib
    responses = httplib.responses
except:
    from http import client
    responses = client.responses
try:
    import urlparse
    parse_qsl = urlparse.parse_qsl
except:
    from urllib import parse
    parse_qsl = parse.parse_qsl


class Request(collections.Mapping):
    '''WSGI request wrapper
    '''
    __slots__ = ('__contains__', '__getitem__', '__iter__', '__len__', 'app',
                 'cookies', 'get', 'headers', 'meta', 'method', 'params',
                 'path', )

    def __init__(self, application, environ):
        '''Init request instance from environment
        '''
        self.app = application
        cookie_loader = SimpleCookie()
        cookie_loader.load(environ['HTTP_COOKIE']
                           if 'HTTP_COOKIE' in environ
                           else '')
        self.cookies = dict(cookie_loader)
        self.headers = {}
        self.meta = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.params = dict([(name, values[0] if len(values) == 1 else values)
                    for name, values in parse_qsl(environ['QUERY_STRING'])])

    def get(self, name, default=None):
        '''Get item from params with default value
        '''
        return name in self.params and self.params[name] or default

    def __contains__(self, name):
        '''Check is variable in request
        '''
        return name in self.params

    def __getitem__(self, name):
        '''Get item from params as from dictionary
        '''
        return self.get(name, None)

    def __iter__(self):
        '''Get iterator over the request params
        '''
        return self.params.iter()

    def __len__(self):
        '''Get the number of items in request
        '''
        return len(self.params)


class Response(object):
    '''Class represents response
    '''
    __slots__ = ('__init__', '__str__', 'data', 'code', 'headers', 'status', )

    def __init__(self, data='', code=200, headers=None):
        self.data = data
        self.code = code
        self.headers = headers if headers else [('Content-Type', 'text/html')]

    @property
    def status(self):
        '''Get respone status

        Returns:
            status associated with code
        '''
        return ('%s %s' % (self.code, responses[self.code])
                if self.code in responses else '200 OK')

    def finish(self):
        '''Get response string representations

        Returns:
            data stored in response converted to string
        '''
        return str(self.data)
    __str__ = finish
