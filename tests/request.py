'''Test case for whole template
'''
import unittest

from lighty.wsgi.http import Request


class RequestTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        self.environ = {
            'HTTP_COOKIE': 'cookie',
            'REQUEST_METHOD': 'get',
            'PATH_INFO': '/hello/world',
            'QUERY_STRING': 'a=1&b=text',
        }
        self.request = Request(self, self.environ)

    def testApp(self):
        assert self.application == self, 'Error setting response application'

    def testRequestMethod(self):
        assert self.request.method == 'get', ('Wrong request method: %s' % 
                self.request.method)

    def testPathInfo(self):
        assert self.request.path == '/hello/world', ('Wrong request path: %s' %
                self.request.path)

    def testCookies(self):
        # TODO: write valid code
        assert self.request.cookies == 'cookie', ('Wrong cookies string: %s' %
                self.request.cookies)

    def testHeaders(self):
        # TODO: write valid code here
        pass

    def testRequestParams(self):
        '''Check all the methods to access request as params
        '''
        assert self.request.params['a'] == '1', ('Wrong param "a" value: %s' %
                self.request.params['a'])
        assert self.request.params['b'] == 'text', (
                'Wrong param "b" value: %s' % self.request.params['b'])

    def testRequestParamsAccess(self):
        '''Check all the methods to access request as params
        '''
        assert self.request['a'] == '1', ('Wrong param "a" value: %s' %
                self.request['a'])
        assert self.request['b'] == 'text', ('Wrong param "b" value: %s' %
                self.request['b'])
        assert 'a' in self.request, '"a" param was not found in request'



def test():
    suite = unittest.TestSuite()
    suite.addTest(RequestTestCase('testApp'))
    suite.addTest(RequestTestCase('testRequestMethod'))
    suite.addTest(RequestTestCase('testPathInfo'))
    suite.addTest(RequestTestCase('testCookies'))
    suite.addTest(RequestTestCase('testHeaders'))
    suite.addTest(RequestTestCase('testRequestParams'))
    suite.addTest(RequestTestCase('testRequestParamsAccess'))
    return suite
