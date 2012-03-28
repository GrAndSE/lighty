from wsgiref.simple_server import make_server
from .handler import WSGIApplication


def run_server(settings):
    application = WSGIApplication(settings)
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
