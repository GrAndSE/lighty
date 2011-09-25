from wsgiref.simple_server import make_server
from handler import WSGIApplication

def run_server():
    application = WSGIApplication()
    httpd = make_server('', 8000, application.handler)
    print "Serving on port 8000..."
    httpd.serve_forever()
