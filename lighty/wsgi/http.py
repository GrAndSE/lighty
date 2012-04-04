'''Module contains methods to work with request and response objects
'''
import collections
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
    __slots__ = ('__contains__', '__getitem__', '__iter__', '__len__',
                 'application', 'cookies', 'get', 'headers', 'meta', 'method',
                 'params', 'path', )

    def __init__(self, application, environ):
        '''Init request instance from environment
        '''
        print [(k, environ[k]) for k in environ if k.startswith('HTTP')]
        self.application = application
        self.cookies = (dict([c.split('=', 1)
                              for c in environ['HTTP_COOKIE'].split('; ')])
                        if 'HTTP_COOKIE' in environ
                        else {})
        self.headers = {}
        self.meta = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.params = urlparse.parse_qs(environ['QUERY_STRING'])

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


def response(start_response_func, data, status='200 Ok',
             headers=[('Content-type', 'text/html')]):
    '''Make response object
    '''
    headers.append(('Content-Length', str(len(data))))
    start_response_func(status, headers)
    return data
