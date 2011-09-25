'''Declare base exceptions for framework
'''


class NotFoundException(Exception):
    '''Exception thrown when object was not found. Usually to process this 
    exception you just need to create response with 404 error code
    '''

    def __init__(self, msg):
        '''Create new NotFoundException instance
        '''
        self.msg	= msg

    def __str__(self):
        '''Convert to string
        '''
        return self.msg

    def __repr__(self):
        '''Console representation
        '''
        return str(self)


class ApplicationException(Exception):
    '''Exception thrown when something goes wrong in code - need to create page
    with 500 HTTP response.
    '''

    def __init__(self, msg):
        '''Create new ApplicationException instance.
        '''
        self.msg	= msg

    def __str__(self):
        '''Convert to string
        '''
        return self.msg

    def __repr__(self):
        '''Console representation
        '''
        return str(self)
