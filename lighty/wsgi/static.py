'''Provide simple view to serve a static files
'''
import mimetypes
import os.path

from . import http, urls

mimetypes.init()


def static_view(request, path=None):
    '''Serve static files
    '''
    # Get static_root 
    settings = request.app.settings
    static_url = (settings.static_url if settings.static_url.endswith('/')
                  else settings.static_url + '/')
    static_root = os.path.realpath(settings.static_root)
    # Get file path
    if not path:
        url = request.meta['HTTP_HOST'] + request.path
        if not url.startswith(static_url):
            return http.Response('%s was not found' % url, 404)
        file_path = os.path.join(static_root, url.replace(static_url, ''))
    else:
        file_path = os.path.join(static_root, path)
    # Try to open and read file
    with open(file_path, 'rb') as file:
        result = "".join(file.readlines())
        headers = None
        if '.' in file_path:
            _, ext = os.path.splitext(file_path)
            if ext in mimetypes.types_map:
                headers = [('Content-Type', mimetypes.types_map[ext])]
        if not headers:
            headers = [('Content-Type', 'text/html')]
        return http.Response(result, 200, headers)


static_patterns = (
        urls.url('/<path:path>', static_view),
)
