'''Test case for whole template
'''
import unittest

from lighty.templates import Template


class PartialTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        base_template = Template(name="base")
        base_template.parse('{{ now }}{{ future }}')
        self.partial_template = base_template.partial({'now': 'Hello'}, 'part')

    def testPartialName(self):
        assert self.partial_template.name == 'part', 'Wrong name: %s' % (
                self.partial_template.name,)

    def testPartialCommands(self):
        assert len(self.partial_template.commands) == 2, 'Error: %s' % (
                'result template must consists of 2 commands', )

    def testPartialExecution(self):
        result = self.partial_template({'future': ', world!'})
        expected = 'Hello, world!'
        assert result == expected, 'Wrong partial result call: %s' % ''.join(
                    ('"', result, '" except "', expected, '"', ))


def test():
    suite = unittest.TestSuite()
    suite.addTest(PartialTestCase('testPartialName'))
    suite.addTest(PartialTestCase('testPartialCommands'))
    suite.addTest(PartialTestCase('testPartialExecution'))
    return suite
