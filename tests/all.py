import unittest

from tests import tests

def test():
    suite = unittest.TestSuite()
    for test in tests:
        name        = 'tests.' + test
        module      = __import__(name, globals(), locals(), 'test')
        function    = getattr(module, 'test')
        if not callable(function):
            raise AttributeError('%s.%s is not callable' % (name, 'test'))
        for t in function():
            suite.addTest(t)
    return suite
