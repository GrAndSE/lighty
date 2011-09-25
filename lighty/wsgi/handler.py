# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def handler(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    return ret
