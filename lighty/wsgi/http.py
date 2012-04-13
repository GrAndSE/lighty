'''Module contains methods to work with request and response objects
'''
import collections
import Cookie
import httplib
import urlparse
try:
    import cStringIO
    StringIO = cStringIO.StringIO
except:
    try:
        import StringIO as IO
        StringIO = IO.StringIO
    except:
        import io
        StringIO = io.StringIO


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
        cookie_loader = Cookie.SimpleCookie()
        cookie_loader.load(environ['HTTP_COOKIE']
                           if 'HTTP_COOKIE' in environ
                           else '')
        self.cookies = dict(cookie_loader)
        self.headers = {}
        self.meta = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.params = dict([(name, values[0] if len(values) == 1 else values)
            for name, values in urlparse.parse_qsl(environ['QUERY_STRING'])])

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
    __slots__ = ('data', 'code', 'headers', 'status', )

    def __init__(self, data='', code=200,
                 headers=[('Content-Type', 'text/html')]):
        self.data = data
        self.code = code
        self.headers = headers

    @property
    def status(self):
        '''Get respone status

        Returns:
            status associated with code
        '''
        return ('%s %s' % (self.code, httplib.responses[self.code])
                if self.code in httplib.responses else '200 OK')

    def __str__(self):
        '''Get response string representations

        Returns:
            data stored in response converted to string
        '''
        return str(self.data)
