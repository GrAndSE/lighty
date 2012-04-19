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

    def baseAppTest(self, application):
        '''Base application tests
        '''
        from .urlpatterns import hello
        func = application.resolve_url('/hello').func
        assert func == hello, 'Error resolving url for /hello: %s' % func
        value = application.settings.value
        assert value == 'test', 'Error get value from app settings: %s' % value

    def testBaseApp(self):
        '''Test BaseApplication class from lighty.wsgi
        '''
        application = BaseApplication(self.settings)
        self.baseAppTest(application)

    def testComplexApp(self):
        '''Test ComplexApplication class from lighty.wsgi
        '''
        application = ComplexApplication(self.settings)
        self.baseAppTest(application)
        from lighty.templates import loaders
        assert (isinstance(application.template_loader, loaders.FSLoader),
                'Error template loader creation')
        assert application.get_template, 'Error get_template() app method'


def test():
    suite = unittest.TestSuite()
    suite.addTest(WSGIApplicationTestCase('testBaseApp'))
    suite.addTest(WSGIApplicationTestCase('testComplexApp'))
    return suite
