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

    # numerical filters

    def testSum(self):
        '''Test sum template filter'''
        result = templatefilters.sum(1, 2, 3, 4)
        self.assertResult('sum', result, 10)

    def testFloatFormat(self):
        '''Test floatformat template filter'''
        value = '12.45'
        result = templatefilters.floatformat(value)
        self.assertResult('floatformat("%s")' % value, result, '12')
        result = templatefilters.floatformat(value, '1')
        self.assertResult('floatformat("%s")' % value, result, '12.4')
        result = templatefilters.floatformat(value, '4')
        self.assertResult('floatformat("%s")' % value, result, '12.4500')
        result = templatefilters.floatformat(value, '-4')
        self.assertResult('floatformat("%s")' % value, result, '12.45')

    def testFloatRound(self):
        '''Test floatround template filter'''
        value = '12.45'
        result = templatefilters.floatround(value)
        self.assertResult('floatround("%s")' % value, result, Decimal('12'))
        result = templatefilters.floatround(value, '1')
        self.assertResult('floatround("%s")' % value, result, Decimal('12.5'))

    # string filters

    def testUpper(self):
        '''Test upper template filter'''
        result = templatefilters.upper('hello')
        self.assertResult('upper("hello")', result, 'HELLO')

    def testLower(self):
        '''Test lower template filter'''
        result = templatefilters.lower('hello')
        self.assertResult('lower("HELLO")', result, 'hello')

    def testCapfirst(self):
        '''Test capfirst template filter'''
        result = templatefilters.capfirst('hello')
        self.assertResult('capfirst("hello")', result, 'Hello')

    def testAddSlashes(self):
        '''Test addslashes template filter'''
        value = '"Hello\\goodbue \'master\'"'
        result = templatefilters.addslashes(value)
        expected = '\\"Hello\\\\goodbue \\\'master\\\'\\"'
        self.assertResult('addslashes("%s")' % value, result, expected)

    def testStringFormat(self):
        '''Test stringformat template filter'''
        format = '4f'
        value = 3.14
        name = 'stringformat(%s, "%s")' % (value, format)
        result = templatefilters.stringformat(value, format)
        self.assertResult(name, result, '%4f' % value)

    # list filters

    def testJoin(self):
        '''Test join template filter'''
        value = (1, 2, 3, 4)
        result = templatefilters.join(value, ',')
        self.assertResult('join(%s)' % str(value), result, '1,2,3,4')

    def testLength(self):
        '''Test length template filter'''
        value = (1, 2, 3, 4)
        result = templatefilters.length(value)
        self.assertResult('length(%s)' % str(value), result, 4)

    def testFirst(self):
        '''Test first template filter'''
        value = (1, 2, 3, 4)
        result = templatefilters.first(value)
        self.assertResult('first(%s)' % str(value), result, 1)
        value = {'first': 1, 'last': 4}
        result = templatefilters.first(value)
        self.assertResult('first(%s)' % str(value), result, 1)

    def testLast(self):
        '''Test last template filter'''
        value = (1, 2, 3, 4)
        result = templatefilters.last(value)
        self.assertResult('last(%s)' % str(value), result, 4)
        value = {'first': 1, 'last': 4}
        result = templatefilters.last(value)
        self.assertResult('last(%s)' % str(value), result, 4)

    def testSort(self):
        '''Test sort template filter'''
        value = (4, 5, 3, 1, 2)
        result = templatefilters.sort(value)
        self.assertResult('sort(%s)' % str(value), result, [1, 2, 3, 4, 5])
        result = templatefilters.sort(value, order=True)
        self.assertResult('sort(%s, order=True)' % str(value), result,
                          [5, 4, 3, 2, 1])

    def testDictSort(self):
        '''Test dictsort template filter'''
        value = ({'name': 'first', 'age': 12},
                 {'name': 'second', 'age': 10},
                 {'name': 'third', 'age': 11})
        result = templatefilters.dictsort(value, 'age')
        self.assertResult('dictsort(%s)' % str(value), result,
                          [{'name': 'second', 'age': 10},
                           {'name': 'third', 'age': 11},
                           {'name': 'first', 'age': 12}])
        result = templatefilters.dictsort(value, 'age', order=True)
        self.assertResult('dictsort(%s, order=True)' % str(value), result,
                          [{'name': 'first', 'age': 12},
                           {'name': 'third', 'age': 11},
                           {'name': 'second', 'age': 10}])

    # Date

    def testDate(self):
        '''Test data format string
        '''
        import datetime
        value = datetime.datetime(2008, 9, 3, 20, 56, 35)
        format = "%Y-%m-%dT%H:%M:%S"
        result = templatefilters.date(value, format)
        self.assertResult('date("%s", "%s")' % (str(value), format), result,
                          '2008-09-03T20:56:35')


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
    suite.addTest(DefaultFiltersTestCase('testJoin'))
    suite.addTest(DefaultFiltersTestCase('testLength'))
    suite.addTest(DefaultFiltersTestCase('testFirst'))
    suite.addTest(DefaultFiltersTestCase('testLast'))
    suite.addTest(DefaultFiltersTestCase('testSort'))
    suite.addTest(DefaultFiltersTestCase('testDictSort'))
    suite.addTest(DefaultFiltersTestCase('testDate'))
    return suite
