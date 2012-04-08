import functools

from .http import Request, response
from .urls import url


def handler(application, resolve_url, environ, start_response):
    '''Create request object, resolve url, execute view and send response
    '''
    request = Request(application, environ)
    view = resolve_url(environ['PATH_INFO'], environ['REQUEST_METHOD'])
    response_func = functools.partial(response, start_response)
    result = view(request)
    return response_func(str(result), result.code)


def static_view(request, path):
    '''Serve static files
    '''
    with open(path, 'rb') as file:
        return "".join(file.readlines())


static_patterns = (
        url('/<path:path>', static_view),
)
