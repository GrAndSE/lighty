'''Commands can be used to easy run server or create an application
'''
import functools

def make_application(settings):
    from . import ComplexApplication
    from .handler import handler
    application = ComplexApplication(settings)
    return functools.partial(handler, application, application.resolve_url)


def run_server(settings):
    '''Run application using wsgiref test server
    '''
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, make_application(settings))
    print("Serving on port 8000...")
    httpd.serve_forever()


def run_tornado(settings):
    '''Run application using Tornade Web framework WSGI server
    '''
    from tornado import ioloop, httpserver, wsgi
    container = wsgi.WSGIContainer(make_application(settings))
    http_server = httpserver.HTTPServer(container)
    http_server.listen(8000)
    print("Serving on port 8000...")
    ioloop.IOLoop.instance().start()
