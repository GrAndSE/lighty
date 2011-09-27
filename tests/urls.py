'''Test case for whole template
'''
import unittest

from lighty.wsgi.urls import resolve, url

def no_arg_func(): return ''
def one_arg_func(arg): return str(arg)
def one_arg_func_float(arg): return str(arg)
def one_arg_func_char(arg): return str(arg)
def one_arg_func_int(arg): return str(arg)
def one_arg_func_str(arg): return str(arg)
def two_arg_func(f, s): return str(f) + str(s)


class PatternMatchingTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        self.urls = (
                url('/test/', 'tests.urls.no_arg_func'),
                url('/arg/<id:int>', 'tests.urls.one_arg_func_int'),
                url('/arg/<letter:char>', 'tests.urls.one_arg_func_char'),
                url('/arg/<number:float>', 'tests.urls.one_arg_func_float'),
                url('/arg/<alias:str>', 'tests.urls.one_arg_func_str'),
                url('/default_arg/<key>/', 'tests.urls.one_arg_func'),
                url('/args/<action>/<id>/', 'tests.urls.two_arg_func'),
        )

    def testSimpleUrl(self):
        func = resolve(self.urls, '/test/', method='GET').func
        assert func == no_arg_func, 'No arguments function for /test/ required'

    def testIntArgUrl(self):
        func = resolve(self.urls, '/arg/12', method='GET').func
        assert func == one_arg_func_int, 'Non int argument function for /arg/12'

    def testFloatArgUrl(self):
        func = resolve(self.urls, '/arg/12.3', method='GET').func
        assert func == one_arg_func_float, 'Non float argument function for /arg/12.3'

    def testCharArgUrl(self):
        func = resolve(self.urls, '/arg/a', method='GET').func
        assert func == one_arg_func_char, 'Non char argument function for /arg/12'

    def testStrArgUrl(self):
        func = resolve(self.urls, '/arg/a-1', method='GET').func
        assert func == one_arg_func_str, 'Non str argument function for /arg/12'


def test():
    suite = unittest.TestSuite()
    suite.addTest(PatternMatchingTestCase('testSimpleUrl'))
    suite.addTest(PatternMatchingTestCase('testCharArgUrl'))
    suite.addTest(PatternMatchingTestCase('testIntArgUrl'))
    suite.addTest(PatternMatchingTestCase('testFloatArgUrl'))
    suite.addTest(PatternMatchingTestCase('testStrArgUrl'))
    return suite
