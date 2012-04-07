'''Test case for Request class
'''
import unittest

from lighty.wsgi.http import Request

CSRFTOKEN = '48831b11aea954cd93464468553ecc6c'
CLTRACK = 'rbr6t7nud3etn90f38j3f3n4i2'
UTMA = '96992031.112838200.1323767133.1330596387.1330599154.22'
UTMZ = '96992031.1323767133.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
COOKIE_STRING = 'CLTRACK=%s; __utma=%s; __utmz=%s; csrftoken=%s' % (CLTRACK,
        UTMA, UTMZ, CSRFTOKEN)


class RequestTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        self.environ = {
            'HTTP_COOKIE': COOKIE_STRING,
            'REQUEST_METHOD': 'get',
            'PATH_INFO': '/hello/world',
            'QUERY_STRING': 'a=1&b=text',
        }
        self.request = Request(self, self.environ)

    def testApp(self):
        assert self.request.app == self, 'Error setting response application'

    def testRequestMethod(self):
        assert self.request.method == 'get', ('Wrong request method: %s' % 
                self.request.method)

    def testPathInfo(self):
        assert self.request.path == '/hello/world', ('Wrong request path: %s' %
                self.request.path)

    def testCookies(self):
        assert self.request.cookies['csrftoken'].value == CSRFTOKEN, (
                    'Wrong cookie "csrftoken": %s' %
                    self.request.cookies['csrftoken'].value)
        assert self.request.cookies['CLTRACK'].value == CLTRACK, (
                    'Wrong cookie "CLTRACK": %s' %
                    self.request.cookies['CLTRACK'].value)


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
