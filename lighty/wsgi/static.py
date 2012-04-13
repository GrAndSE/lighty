import mimetypes
import os.path

from . import http, urls

mimetypes.init()


def static_view(request, path):
    '''Serve static files
    '''
    settings = request.app.settings
    url = request.meta['HTTP_HOST'] + request.path
    static_url = (settings.static_url if settings.static_url.endswith('/')
                  else settings.static_url + '/')
    static_root = os.path.realpath(settings.static_root)
    file_path = os.path.join(static_root, url.replace(static_url, ''))
    with open(file_path, 'rb') as file:
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
