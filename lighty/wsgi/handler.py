from functools import partial

from lighty.exceptions import ApplicationException, NotFoundException

from http import Request, Response
from urls import resolve, url


def test():
    return 'All ok'

class WSGIApplication(object):
    '''Main application handler
    '''

    def __init__(self):
        '''Create new application handler instance
        '''
        super(WSGIApplication, self).__init__()
        urls = (
                url('/hello', 'lighty.wsgi.handler.test'),
        )
        self.resolve = partial(resolve, urls)

    
    def handler(self, environ, start_response):
        '''Basic function for responsing
        '''
        # Create new request and process middleware
        view    = self.resolve(environ['PATH_INFO'], environ['REQUEST_METHOD'])
        response = Response(issubclass(view.__class__, Exception) and str(view)
                            or view())
        response.status = ((view.__class__ == NotFoundException and
                                '404 Page was not found') or
                           (view.__class__ == ApplicationException and
                                '500 Internal Server Error') or
                           (view.__class__ == ApplicationException and
                                '500 Internal Server Error') or
                           '200 OK')
        yield response.start(start_response)
