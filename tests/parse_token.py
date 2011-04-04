"""parse_token test case"""

import unittest

from lighty.templates.tag import parse_token

class FormFieldsTestCase(unittest.TestCase):
    ''' Test form fields '''

    def setUp(self):
        # Test Field class
        pass

    def testCleanBrackets(self):
        parsed = parse_token('"test.html"')
        needed = ['test.html'] 
        assert parsed == needed, 'Brackets cleaning failed: %s except %s' % (
                                 parsed, needed)

    def testCleanInnerBrackets(self):
        parsed = parse_token('"test\'html"')
        needed = ['test\'html']
        assert parsed == needed, 'Brackets cleaning failed: %s except %s' % (
                                 parsed, needed)

    def testParseSimpleTokens(self):
        parsed = parse_token('a in b')
        needed = ['a', 'in', 'b']
        assert parsed == needed, 'Token parsing failed: %s except %s' % (
                                 parsed, needed)

    def testParseTokensWithSentence(self):
        parsed = parse_token('a as "Let me in"')
        needed = ['a', 'as', 'Let me in']
        assert parsed == needed, 'Token with sentence parsing failed: %s' % (
                                 ' '.join((parsed, 'except', needed)))
