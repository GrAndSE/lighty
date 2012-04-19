'''Test case for wsgi application loading process

No includes test for ComplexApllication that checks is apps was loaded and is
template dirs included
'''
import unittest

from lighty.conf import Settings
from lighty.wsgi import BaseApplication, ComplexApplication


class WSGIApplicationTestCase(unittest.TestCase):
    '''Test case for application loading
    '''

    def setUp(self):
        '''Load settings for application loading
        '''
        self.settings = Settings('tests/test.cfg')

    def testBaseApp(self):
        '''Test BaseApplication class from lighty.wsgi
        '''
        pass

    def testComplexApp(self):
        '''Test ComplexApllication class from lighty.wsgi
        '''
        pass


def test():
    suite = unittest.TestSuite()
    suite.addTest(WSGIApplicationTestCase('testBaseApp'))
    suite.addTest(WSGIApplicationTestCase('testComplexApp'))
    return suite
