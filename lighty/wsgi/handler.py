from lighty.exceptions import ApplicationException, NotFoundException


class WSGIApplication(object):
    '''Main application handler
    '''

    def __init__(self):
        '''Create new application handler instance
        '''
        super(WSGIApplication, self).__init__()

    
    def handler(self, environ, start_response):
        '''Basic function for responsing
        '''
        headers = [('Content-type', 'text/plain')]

        try:
            # Create new request and process middleware
            status = '200 OK'
            msg = 'All is fine'
        except NotFoundException as exc:
            status = '404 Page was now found'
            msg = str(exc)
        except ApplicationException as exc:
            status = '500 Internal Server Error'
            msg = str(exc)
        finally:
            start_response(status, headers)
            return status + '\n' + msg

