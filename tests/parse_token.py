"""parse_token test case"""

import unittest

from lighty.templates.tag import parse_token, VARIABLE, STRING, NUMBER

class ParseTokenTestCase(unittest.TestCase):
    ''' Test form fields '''

    def setUp(self):
        # Test Field class
        pass

    def testCleanBrackets(self):
        parsed = parse_token('"test.html"')
        needed = ['test.html'], [STRING]
        assert parsed == needed, 'Brackets cleaning failed: %s except %s' % (
                                 parsed, needed)

    def testCleanInnerBrackets(self):
        parsed = parse_token('"test\'html"')
        needed = ['test\'html'], [STRING]
        assert parsed == needed, 'Brackets cleaning failed: %s except %s' % (
                                 parsed, needed)

    def testParseSimpleTokens(self):
        parsed = parse_token('a in b')
        needed = ['a', 'in', 'b'], [VARIABLE, VARIABLE, VARIABLE]
        assert parsed == needed, 'Token parsing failed: %s except %s' % (
                                 parsed, needed)

    def testParseTokensWithSentence(self):
        parsed = parse_token('a as "Let me in"')
        needed = ['a', 'as', 'Let me in'], [VARIABLE, VARIABLE, STRING]
        assert parsed == needed, 'Token with sentence parsing failed: %s' % (
                                ' '.join((str(parsed), 'except', str(needed))))

    def testParseTokensWithNumbers(self):
        parsed = parse_token('1 as a')
        needed = ['1', 'as', 'a'], [NUMBER, VARIABLE, VARIABLE]
        assert parsed == needed, 'Token with number parsing failse: %s' % (
                                ' '.join((str(parsed), 'except', str(needed))))


def test():
    suite = unittest.TestSuite()
    suite.addTest(ParseTokenTestCase('testCleanBrackets'))
    suite.addTest(ParseTokenTestCase("testCleanInnerBrackets"))
    suite.addTest(ParseTokenTestCase("testParseSimpleTokens"))
    suite.addTest(ParseTokenTestCase("testParseTokensWithSentence"))
    suite.addTest(ParseTokenTestCase("testParseTokensWithNumbers"))
    return suite
