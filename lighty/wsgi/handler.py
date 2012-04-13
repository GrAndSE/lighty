import mimetypes
import os.path

from .. import monads
from .http import Request
from .urls import url


def handler(application, resolve_url, environ, start_response):
    '''Create request object, resolve url, execute view and send response
    '''
    request = Request(application, environ)
    view = resolve_url(environ['PATH_INFO'], environ['REQUEST_METHOD'])
    response = view(request)
    start_response(response.status, response.headers)
    return str(response)


mimetypes.init()


def static_view(request, path):
    '''Serve static files
    '''
    with open(path, 'rb') as file:
        result = monads.ValueMonad("".join(file.readlines()), 200)
        if '.' in path:
            _, ext = os.path.splitext(path)
            if ext in mimetypes.types_map:
                result.headers = [('Content-Type', mimetypes.types_map[ext])]
        if hasattr(result, 'headers'):
            result.headers = [('Content-Type', 'text/html')]
        return result


static_patterns = (
        url('/<path:path>', static_view),
)
