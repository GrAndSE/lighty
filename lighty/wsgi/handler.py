import collections
import functools

from .http import Request, response
from .urls import url


def handler(application, resolve_url, environ, start_response):
    '''Basic function for responsing
    '''
    # Create new request and process middleware
    view = resolve_url(environ['PATH_INFO'], environ['REQUEST_METHOD'])
    status = ((issubclass(view.__class__, LookupError) and
               '404 Page was now found') or
              (issubclass(view.__class__, Exception) and
               '500 Internal Server Error') or
              '200 OK')
    response_func = functools.partial(response, start_response)
    data = (view(request=Request(application, environ))
            if isinstance(view, collections.Callable)
            else str(view))
    return response_func(data, status)


def static_view(request, path):
    with open(path, 'rb') as file:
        return "".join(file.readlines())


static_patterns = (
        url('/<path:path>', static_view),
)
