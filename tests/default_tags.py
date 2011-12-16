'''Module to test default template tags such as if, for, with, include, etc.
'''
import unittest

from lighty.templates import Template


class DefaultTagsTestCase(unittest.TestCase):
    """Test case for if template tag
    """

    def assertResult(self, name, result, value):
        assert result == value, 'Error on tag "%s" applying to: %s' % (
                           name, ' '.join((str(result), 'except', str(value))))

    def testSimpleIf(self):
        template = Template()
        template.parse('{% if a %}Foo{% endif %}')
        true_context = {'a': 1}
        result = template(true_context)
        self.assertResult('if', result.strip(), 'Foo')


def test():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTagsTestCase('testSimpleIf'))
    return suite
