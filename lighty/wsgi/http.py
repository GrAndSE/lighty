try:
    import cStringIO as StringIO
except:
#    try:
#        import StringIO
#    except:
#        import io as StringIO
    pass

class Request(object):
    '''WSGI request wrapper
    '''
    __slots__ = ('method', 'headers', 'cookies', 'path', 'params', 'get')

    def __init__(self, environ):
        self.protocol   = environ['SERVER_PROTOCOL']
        self.method     = environ['REQUEST_METHOD']
        self.path       = environ['PATH_INFO']
        self.query      = environ['QUERY_STRING']
        #self.accept_lan = environ['HTTP_ACCEPT_LANGUAGE']
        #self.accept_chr = environ['HTTP_ACCEPT_CHARSET']
        #self.accept     = environ['HTTP_ACCEPT']
        #self.cookie     = environ['HTTP_COOKIE']
        #self.params = {}
        # 'CONTENT_LENGTH': '', 'HTTP_CONNECTION': 'keep-alive', 'CONTENT_TYPE': 'text/plain', 'SSH_AUTH_SOCK': '/tmp/keyring-qn1yMR/ssh', 'wsgi.multithread': True, 'GDMSESSION': 'ubuntu-2d', 'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0) Gecko/20100101 Firefox/7.0', 'HTTP_HOST': '127.0.0.1:8000'
        # 'REMOTE_HOST': 'localhost', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate',

    def get(self, name, default=None):
        return name in self.params and self.params[name] or default


class Response(object):
    '''Class used to put data into response
    '''
    __slots__ = ('buffer', 'write', 'headers', 'cookies', 'status', 'start')

    def __init__(self, data, content_type='text/html'):
        self.status     = '200 OK'
        self.headers    = [('Content-type', content_type)]
        self.buffer     = StringIO.StringIO()
        self.buffer.write(data)

    def start(self, start_response_func):
        result_data = self.buffer.getvalue()
        self.buffer.close()
        self.headers.append(('Content-Length', str(len(result_data))))
        start_response_func(self.status, self.headers)
        return result_data
