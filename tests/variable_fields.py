"""Test cases for variable fields
"""
import unittest

from lighty.templates import Template


class VariableFieldTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def setUp(self):
        self.value = 'value'
        self.variable_template = Template(name='base.html')
        self.variable_template.parse("{{ simple_var }}")
        self.object_field_template = Template(name='object-field.html')
        self.object_field_template.parse('{{ object.field }}')
        self.deep_template = Template(name='deep-field.html')
        self.deep_template.parse('{{ object.field.field }}')

    def assertResult(self, result):
        assert result == self.value, 'Error emplate execution: %s' % ' '.join((
                                     result, 'except', self.value))

    def testSimpleVariable(self):
        result = self.variable_template.execute({'simple_var': 'value'})
        self.assertResult(result)

    def testObjectField(self):
        class TestClass(object):
            field = self.value
        result = self.object_field_template.execute({'object': TestClass()})
        self.assertResult(result)

    def testDictValue(self):
        obj = {'field': self.value }
        result = self.object_field_template.execute({'object': obj})
        self.assertResult(result)

    def testMultilevelField(self):
        class TestClass(object):
            field = {'field': self.value}
        result = self.deep_template.execute({'object': TestClass()})
        self.assertResult(result)


def test():
    suite = unittest.TestSuite()
    suite.addTest(VariableFieldTestCase('testSimpleVariable'))
    suite.addTest(VariableFieldTestCase('testObjectField'))
    suite.addTest(VariableFieldTestCase('testDictValue'))
    suite.addTest(VariableFieldTestCase('testMultilevelField'))
    return suite
