from .http import Request


def handler(application, resolve_url, environ, start_response):
    '''Create request object, resolve url, execute view and send response
    '''
    request = Request(application, environ)
    view = resolve_url(environ['PATH_INFO'], environ['REQUEST_METHOD'])
    response = view(request)
    start_response(response.status, response.headers)
    return str(response)
