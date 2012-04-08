

def run_server(settings):
    '''Run application using wsgiref test server
    '''
    from wsgiref.simple_server import make_server
    from . import WSGIApplication
    application = WSGIApplication(settings)
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()


def run_tornado(settings):
    '''Run application using Tornade Web framework WSGI server
    '''
    from tornado import ioloop, httpserver, wsgi
    from . import WSGIApplication
    application = WSGIApplication(settings)
    container = wsgi.WSGIContainer(application)
    http_server = httpserver.HTTPServer(container)
    http_server.listen(8000)
    ioloop.IOLoop.instance().start()
