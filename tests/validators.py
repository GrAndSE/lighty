"""Test cases for variable fields
"""
import unittest

from lighty.monads import ErrorMonad
from lighty.validators import Validator, validate


class TrueFalseValidator(Validator):
    def check(self, value):
        return value if value else self.error(value)


class CustomErrorMessageValidator(TrueFalseValidator):
    def message(self, value):
        return 'Value: %s' % value


class ValidatorTestCase(unittest.TestCase):
    """Test case for Validator class and validate function
    """

    def testSimpleValidator(self):
        '''Test simplest validator
        '''
        validator = TrueFalseValidator()
        assert validator(True), 'Error validating True or False'
        assert isinstance(validator(False), ErrorMonad), ('Wrong validation '
                'result type')
        assert str(validator(False)) == 'Validation error', (
                'Wrong validation default error message')


    def testCustomErrorMessage(self):
        '''Test validator with customized error message format
        '''
        validator = TrueFalseValidator('Value equals to False')
        message = str(validator(False))
        assert message == 'Value equals to False', (
                'Wrong validation custom error message: %s' % message)
        validator = CustomErrorMessageValidator()
        message = str(validator(False))
        assert message == 'Value: False', (
                'Wrong validation custom error message: %s' % message)


def test():
    suite = unittest.TestSuite()
    suite.addTest(ValidatorTestCase('testSimpleValidator'))
    suite.addTest(ValidatorTestCase('testCustomErrorMessage'))
    return suite
