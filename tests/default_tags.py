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

    def testSpacelless(self):
        template = Template()
        template.parse('''{% spaceless %}
                        Some 
                            broken 
                    text
                {% endspaceless %}''')
        result = template({})
        right = 'Some broken text'
        assert result == right, 'Spaceless tag error:\n%s' % (
                                    "\n".join(result, 'except', right))

    def testSimpleIf(self):
        template = Template()
        template.parse('{% if a %}Foo{% endif %}')
        result = template({'a': 1})
        self.assertResult('if', result.strip(), 'Foo')
        result = template({'a': 0})
        self.assertResult('if', result.strip(), '')

    def testSimpleFor(self):
        template = Template()
        template.parse('{% for a in list %}{{ a }} {% endfor %}')
        result = template({'list': [1, 2, 3, 4, 5]})
        self.assertResult('for', result.strip(), '1 2 3 4 5')



def test():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTagsTestCase('testSpacelless'))
    suite.addTest(DefaultTagsTestCase('testSimpleIf'))
    suite.addTest(DefaultTagsTestCase('testSimpleFor'))
    return suite
