'''Module to test default template filters
'''
import unittest
from decimal import Decimal

from lighty.templates import templatefilters


class DefaultFiltersTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def assertResult(self, name, result, value):
        assert result == value, 'Error on filter "%s" applying: %s' % (
                           name, ' '.join((str(result), 'except', str(value))))

    def testSum(self):
        result = templatefilters.sum(1, 2, 3, 4)
        self.assertResult('sum', result, 10)

    def testFloatFormat(self):
        value   = '12.45'
        result  = templatefilters.floatformat(value)
        self.assertResult('floatformat("%s")' % value, result, '12')
        result  = templatefilters.floatformat(value, '1')
        self.assertResult('floatformat("%s")' % value, result, '12.4')
        result  = templatefilters.floatformat(value, '4')
        self.assertResult('floatformat("%s")' % value, result, '12.4500')
        result  = templatefilters.floatformat(value, '-4')
        self.assertResult('floatformat("%s")' % value, result, '12.45')

    def testFloatRound(self):
        value   = '12.45'
        result  = templatefilters.floatround(value)
        self.assertResult('floatround("%s")' % value, result, Decimal('12'))
        result  = templatefilters.floatround(value, '1')
        self.assertResult('floatround("%s")' % value, result, Decimal('12.5'))

    def testUpper(self):
        result  = templatefilters.upper('hello')
        self.assertResult('upper("hello")', result, 'HELLO')

    def testLower(self):
        result  = templatefilters.lower('hello')
        self.assertResult('lower("HELLO")', result, 'hello')

    def testCapfirst(self):
        result  = templatefilters.capfirst('hello')
        self.assertResult('capfirst("hello")', result, 'Hello')

    def testAddSlashes(self):
        value   = '"Hello\\goodbue \'master\'"'
        result  = templatefilters.addslashes(value)
        expected= '\\"Hello\\\\goodbue \\\'master\\\'\\"'
        self.assertResult('addslashes("%s")' % value, result, expected)

    def testStringFormat(self):
        format  = '4f'
        value   = 3.14
        name    = 'stringformat(%s, "%s")' % (value, format)
        result  = templatefilters.stringformat(value, format)
        self.assertResult(name, result, '%4f' % value)



def test():
    suite = unittest.TestSuite()
    suite.addTest(DefaultFiltersTestCase('testSum'))
    suite.addTest(DefaultFiltersTestCase('testFloatFormat'))
    suite.addTest(DefaultFiltersTestCase('testFloatRound'))
    suite.addTest(DefaultFiltersTestCase('testStringFormat'))
    suite.addTest(DefaultFiltersTestCase('testUpper'))
    suite.addTest(DefaultFiltersTestCase('testLower'))
    suite.addTest(DefaultFiltersTestCase('testCapfirst'))
    suite.addTest(DefaultFiltersTestCase('testAddSlashes'))
    return suite
