from wsgiref.simple_server import make_server
from handler import handler

def run_server():
    httpd = make_server('', 8000, handler)
    print "Serving on port 8000..."
    httpd.serve_forever()
