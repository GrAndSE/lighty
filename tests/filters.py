"""Test cases for variable fields
"""
import unittest

from lighty.templates import Template
from lighty.templates.filter import filter_manager


def simple_filter(value):
    return str(value).upper()
filter_manager.register(simple_filter)

def argument_filter(value, arg):
    return str(value) + ', ' + str(arg)
filter_manager.register(argument_filter)

def multiarg_filter(value, *args):
    return ', '.join([str(arg) for arg in (value, ) + args])
filter_manager.register(multiarg_filter)


class TemplateFiltersTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def assertResult(self, result, value):
        assert result == value, 'Error emplate execution: %s' % ' '.join((
                                     result, 'except', value))

    def testSimpleFilter(self):
        simple_template = Template(name='simple-filter.html')
        simple_template.parse("{{ simple_var|simple_filter }}")
        result = simple_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'HELLO')

    def testArgFilter(self):
        argument_template = Template(name='argument-filter.html')
        argument_template.parse('{{ simple_var|argument_filter:"world" }}')
        result = argument_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'Hello, world')

    def testMultiargFilter(self):
        multiarg_template = Template(name='multiarg-filter.html')
        multiarg_template.parse(
                            '{{ simple_var|multiarg_filter:"John" "Peter" }}')
        result = multiarg_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'Hello, John, Peter')


def test():
    suite = unittest.TestSuite()
    suite.addTest(TemplateFiltersTestCase('testSimpleFilter'))
    suite.addTest(TemplateFiltersTestCase('testArgFilter'))
    suite.addTest(TemplateFiltersTestCase('testMultiargFilter'))
    return suite
