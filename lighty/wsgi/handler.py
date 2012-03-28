import sys, traceback

from functools import partial

from lighty.exceptions import ApplicationException, NotFoundException
from urls import resolve, url


def test():
    return 'All ok'

def WSGIApplication(urls):
    '''Create main application handler
    '''
    urls = (
        url('/hello', 'lighty.wsgi.handler.test'),
    )
    resolve_url = partial(resolve, urls)
    
    def handler(resolve_url, environ, start_response):
        '''Basic function for responsing
        '''
        headers = [('Content-type', 'text/plain')]

        try:
            # Create new request and process middleware
            view = resolve_url(environ['PATH_INFO'], environ['REQUEST_METHOD'])
            if issubclass(view.__class__, Exception):
                raise view
            msg = view()
            status = '200 OK'
        except NotFoundException as exc:
            traceback.print_exc(file=sys.stdout)
            status = '404 Page was now found'
            msg = str(exc)
        except ApplicationException as appexc:
            traceback.print_exc(file=sys.stdout)
            status = '500 Internal Server Error'
            msg = appexc and str(appexc)
        except Exception as exc:
            traceback.print_exc(file=sys.stdout)
            status = '500 Internal Server Error'
            msg = str(exc)
        finally:
            start_response(status, headers)
            return status + '\n' + msg
    return partial(handler, resolve_url)
