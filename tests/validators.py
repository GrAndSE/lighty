"""Test cases for variable fields
"""
import unittest

from lighty.monads import ErrorMonad
from lighty.validators import Validator, validate


class TrueFalseValidator(Validator):
    def validate(self, value):
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
                'result type: %s' % type(validator(False)))
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

    def testValidateFunction(self):
        '''Test validate function
        '''
        validators = {'field': [TrueFalseValidator()]}
        results = validate(validators, {'field': True})
        assert results['field'] is True, ('Wrong validation results: %s' %
                                          results)
        results = validate(validators, {'field': False})
        assert isinstance(results['field'], ErrorMonad), (
                'Wrong validation results: %s' % results)


def test():
    suite = unittest.TestSuite()
    suite.addTest(ValidatorTestCase('testSimpleValidator'))
    suite.addTest(ValidatorTestCase('testCustomErrorMessage'))
    suite.addTest(ValidatorTestCase('testValidateFunction'))
    return suite
