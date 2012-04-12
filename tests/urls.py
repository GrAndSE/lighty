'''Test case for whole template
'''
import unittest

from lighty.wsgi.urls import resolve, reverse, url

def no_arg_func(): return ''
def one_arg_func(arg): return str(arg)
def one_arg_func_float(arg): return str(arg)
def one_arg_func_char(arg): return str(arg)
def one_arg_func_int(arg): return str(arg)
def one_arg_func_str(arg): return str(arg)
def two_arg_func(action, id): return str(action) + str(id)
def three_arg_func(app, action, id): return str(app) + str(action) + str(id)


class PatternMatchingTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        self.urls = (
                url('/test/', 'tests.urls.no_arg_func', name='noargs'),
                url('/arg/<id:int>', 'tests.urls.one_arg_func_int',
                    name='onearg'),
                url('/arg/<letter:char>', 'tests.urls.one_arg_func_char'),
                url('/arg/<number:float>', 'tests.urls.one_arg_func_float'),
                url('/arg/<alias:str>', 'tests.urls.one_arg_func_str'),
                url('/default_arg/<key>/', 'tests.urls.one_arg_func'),
                url('/args/<action>/<id>/', 'tests.urls.two_arg_func',
                    name='twoargs'),
                url('/<app>/<action>/<id>/', two_arg_func,
                    constraints={'app': '[\\d]+', 'action': '[\\w]+',
                                 'id': '[\\d]+'}),
        )

    def testSimpleUrl(self):
        '''Test resolving url with no arg'''
        func = resolve(self.urls, '/test/', method='GET').func
        assert func == no_arg_func, 'No arguments function for /test/ required'

    def testIntArgUrl(self):
        '''Test resolving url contains int argument'''
        func = resolve(self.urls, '/arg/12', method='GET').func
        assert func == one_arg_func_int, (
                'Non int argument function for /arg/12')

    def testFloatArgUrl(self):
        '''Test resolving url contains float argument'''
        func = resolve(self.urls, '/arg/12.3', method='GET').func
        assert func == one_arg_func_float, (
                'Non float argument function for /arg/12.3')

    def testCharArgUrl(self):
        '''Test resolving url contains character argument'''
        func = resolve(self.urls, '/arg/a', method='GET').func
        assert func == one_arg_func_char, (
                'Non char argument function for /arg/a')

    def testStrArgUrl(self):
        '''Test resolving url contains string argument'''
        func = resolve(self.urls, '/arg/a-1', method='GET').func
        assert func == one_arg_func_str, (
                'Non str argument function for /arg/a-1')

    def testDefaultArgUrl(self):
        '''Test resolving url with default type argument'''
        func = resolve(self.urls, '/default_arg/adftr/', method='GET').func
        assert func == one_arg_func, (
                'One arg function required for /default_arg/adftr/')

    def testTwoArgUrl(self):
        '''Test resolving url with two arguments'''
        func = resolve(self.urls, '/args/test/7/', method='GET').func
        assert func == two_arg_func, (
                'Two arg function required for /args/test/7/')

    def testNonExistsUrl(self):
        '''Test resolving not existen url'''
        func = resolve(self.urls, '/g/g/g/', method='GET')
        assert not func, 'Resolved with wrong arg for /args/test/g/'


    def testReverseNoArgsUrl(self):
        '''Test reversing url without arguments'''
        url = reverse(self.urls, 'noargs')
        assert url == '/test/', ('Error reversing url for name "noargs": %s' %
                                 url)

    def testReverseOneArgUrl(self):
        '''Test reversing url with one argument'''
        url = reverse(self.urls, 'onearg', {'id': 10})
        assert url == '/arg/10', ('Error reversing url for name "onearg" and '
                                  ' args: {"id": 10}: %s' % url)
        url = reverse(self.urls, 'onearg', {'name': 'Peter'})
        assert not url, ('Error reversing url for name "onearg" and args: '
                         '{"name": "Peter"}: %s' % url)
        url = reverse(self.urls, 'noneonearg', {'id': 10})
        assert not url, ('Error reversing url for name "noneonearg" and args: '
                         '{"id": 10}: %s' % url)

    def testReverseTwoArgUrl(self):
        '''Test reversing url with two arguments'''
        url = reverse(self.urls, 'twoargs', {'action': 'get', 'id': 1})
        assert url == '/args/get/1/', ('Error reversing url for name '
                '"twoargs" and args: {"action": "get", "id": 1}: %s' % url)


def test():
    suite = unittest.TestSuite()
    suite.addTest(PatternMatchingTestCase('testSimpleUrl'))
    suite.addTest(PatternMatchingTestCase('testCharArgUrl'))
    suite.addTest(PatternMatchingTestCase('testIntArgUrl'))
    suite.addTest(PatternMatchingTestCase('testFloatArgUrl'))
    suite.addTest(PatternMatchingTestCase('testStrArgUrl'))
    suite.addTest(PatternMatchingTestCase('testDefaultArgUrl'))
    suite.addTest(PatternMatchingTestCase('testTwoArgUrl'))
    suite.addTest(PatternMatchingTestCase('testReverseNoArgsUrl'))
    suite.addTest(PatternMatchingTestCase('testReverseOneArgUrl'))
    suite.addTest(PatternMatchingTestCase('testReverseTwoArgUrl'))
    return suite
