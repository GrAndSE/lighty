from lighty.exceptions import ApplicationException, NotFoundException

from urls import resolve, url
from functools import partial


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
        headers = [('Content-type', 'text/plain')]


        try:
            # Create new request and process middleware
            print environ
            view    = self.resolve(environ['PATH_INFO'])
            msg     = view()
            status  = '200 OK'
        except NotFoundException as exc:
            status = '404 Page was now found'
            msg = str(exc)
        except ApplicationException as appexc:
            status = '500 Internal Server Error'
            msg = appexc and str(appexc)
        except Exception as exc:
            status = '500 Internal Server Error'
            msg = str(exc)
        finally:
            start_response(status, headers)
            return status + '\n' + msg

