import sys, traceback

from .urls import url


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
    except LookupError as exc:
        traceback.print_exc(file=sys.stdout)
        status = '404 Page was now found'
        msg = str(exc)
    except TypeError as appexc:
        traceback.print_exc(file=sys.stdout)
        status = '500 Internal Server Error'
        msg = appexc and str(appexc)
    except ImportError as appexc:
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


def static_view(path):
    with open(path, 'rb') as file:
        return "".join(file.readlines())

static_patterns = (
        url('/<path:path>', static_view),
)
