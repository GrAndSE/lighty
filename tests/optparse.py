'''Test case for command line parsing
'''
import unittest

from lighty.utils import CommandParser


class OptParseTestCase(unittest.TestCase):
    '''Test case used to check command line parser
    '''

    def setUp(self):
        self.parser = CommandParser(program='test', description='parser test')

    def testFlagOption(self):
        '''Test option parser with one flag option
        '''
        self.parser.add_option('h', optional=True, flag=True, help='help')
        args = self.parser._parse([])
        assert args == {}, 'Error parsing empty args: %s except {}' % args
        args = self.parser.parse(['-h'])
        assert args == {'h': ''}, 'Error parsing one arg: %s' % args

    def testValueOption(self):
        '''Test option parser with values option
        '''
        self.parser.add_option('h', optional=True, flag=False, help='help')
        args = self.parser._parse([])
        assert args == {}, 'Error parsing empty args: %s except {}' % args
        args = self.parser.parse(['-h=test'])
        assert args == {'h': 'test'}, 'Error parsing one arg: %s' % args
        args = self.parser.parse(['-h', 'test'])
        assert args == {'h': 'test'}, 'Error parsing one arg: %s' % args
        args = self.parser.parse(['-h', 'test', 'test'])
        assert args == {'h': 'test'}, 'Error parsing two arg: %s' % args


def test():
    suite = unittest.TestSuite()
    suite.addTest(OptParseTestCase('testFlagOption'))
    suite.addTest(OptParseTestCase('testValueOption'))
    return suite
