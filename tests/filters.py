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
        assert result == value, 'Error template execution: %s' % ' '.join((
                                     result, 'except', value))

    def testSimpleFilter(self):
        '''Test simple template filter function applied to variable'''
        simple_template = Template(name='simple-filter.html')
        simple_template.parse("{{ simple_var|simple_filter }}")
        result = simple_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'HELLO')

    def testStringConstFilter(self):
        '''Test simple template filter function applied to string constant'''
        simple_template = Template(name="consts-filter.html")
        simple_template.parse('{{ "hello"|simple_filter }}')
        result = simple_template.execute({})
        self.assertResult(result, 'HELLO')

    def testNumericConstFilter(self):
        '''Test simple template filter function applied to number'''
        simple_template = Template(name="consts-filter.html")
        simple_template.parse('{{ 1|simple_filter }}')
        result = simple_template.execute({})
        self.assertResult(result, '1')

    def testArgFilter(self):
        '''Test calling template filter with arg value specified'''
        argument_template = Template(name='argument-filter.html')
        argument_template.parse('{{ simple_var|argument_filter:"world" }}')
        result = argument_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'Hello, world')

    def testMultiargFilter(self):
        '''Test calling filter with multiply args'''
        multiarg_template = Template(name='multiarg-filter.html')
        multiarg_template.parse(
                            '{{ simple_var|multiarg_filter:"John" "Peter" }}')
        result = multiarg_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'Hello, John, Peter')

    def testMultiFilter(self):
        '''Test calling sequnce of filters'''
        multifilter_template = Template(name='multifilter.html')
        multifilter_template.parse(
                    '{{ simple_var|simple_filter|argument_filter:"world" }}')
        result = multifilter_template.execute({'simple_var': 'Hello'})
        self.assertResult(result, 'HELLO, world')

    def testVaribaleArgFilter(self):
        '''Test calling filter with variable argument'''
        varargfilter_template = Template(name='vararg-filter.html')
        varargfilter_template.parse('{{ simple_var|argument_filter:arg }}')
        result = varargfilter_template.execute({
                'simple_var': 'Hello',
                'arg': 'world'
        })
        self.assertResult(result, 'Hello, world')


def test():
    suite = unittest.TestSuite()
    suite.addTest(TemplateFiltersTestCase('testSimpleFilter'))
    suite.addTest(TemplateFiltersTestCase('testStringConstFilter'))
    suite.addTest(TemplateFiltersTestCase('testNumericConstFilter'))
    suite.addTest(TemplateFiltersTestCase('testArgFilter'))
    suite.addTest(TemplateFiltersTestCase('testMultiargFilter'))
    suite.addTest(TemplateFiltersTestCase('testMultiFilter'))
    suite.addTest(TemplateFiltersTestCase('testVaribaleArgFilter'))
    return suite
