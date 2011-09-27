'''Test case for whole template
'''
import unittest

from lighty.wsgi.urls import resolve, url

def no_arg_func(): return ''
def one_arg_func(arg): return str(arg)
def two_arg_func(f, s): return str(f) + str(s)


class PatternMatchingTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        self.urls = (
                url('/test/', 'tests.urls.no_arg_func'),
                url('/arg/<id:int>', 'tests.urls.one_arg_func'),
                url('/arg/<letter:char>', 'tests.urls.one_arg_func'),
                url('/arg/<number:float>', 'tests.urls.one_arg_func'),
                url('/arg/<alias:str>', 'tests.urls.one_arg_func'),
                url('/default_arg/<key>/', 'tests.urls.one_arg_func'),
                url('/args/<action>/<id>/', 'tests.urls.two_arg_func'),
        )

    def testSimple(self):
        print self.urls
        print resolve(self.urls, '/test/')


def test():
    suite = unittest.TestSuite()
    suite.addTest(PatternMatchingTestCase('testSimple'))
    return suite
