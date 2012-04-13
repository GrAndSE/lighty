import mimetypes
import os.path

from . import http, urls

mimetypes.init()


def static_view(request, path):
    '''Serve static files
    '''
    with open(path, 'rb') as file:
        result = "".join(file.readlines())
        headers = None
        if '.' in path:
            _, ext = os.path.splitext(path)
            if ext in mimetypes.types_map:
                headers = [('Content-Type', mimetypes.types_map[ext])]
        if not headers:
            headers = [('Content-Type', 'text/html')]
        return http.Response(result, 200, headers)


static_patterns = (
        urls.url('/<path:path>', static_view),
)
