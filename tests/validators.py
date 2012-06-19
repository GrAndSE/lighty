"""Test cases for variable fields
"""
import unittest

from lighty.db import fields, models
from lighty.monads import ErrorMonad
from lighty import utils, validators


class TrueFalseValidator(validators.Validator):
    def validate(self, value):
        return value if value else self.error(value)


class CustomErrorMessageValidator(TrueFalseValidator):
    def message(self, value):
        return 'Value: %s' % value


class TestModel(models.Model):
    name = fields.CharField(unique=True)
    test_type = fields.CharField(choices=[('t', 'test'), ('c', 'test case')])
    positive = fields.PositiveIntegerField()


class ValidatorClassTestCase(unittest.TestCase):
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


class ValidatorsTestCase(unittest.TestCase):
    '''Test case for standart validators included in distribution
    '''

    def testChoicesValidator(self):
        '''Test ChoicesValidator class
        '''
        validator = validators.ChoicesValidator([(1, 'One'), (2, 'Two')])
        result = validator(1)
        assert result, 'Unexpected validation error: %s' % result
        result = validator(2)
        assert result, 'Unexpected validation error: %s' % result
        result = validator(3)
        assert not result, 'Validation error missed: %s' % result


class ModelValidatorsTestCase(unittest.TestCase):
    '''Test case to check model validators
    '''

    def testModelValidator(self):
        '''Test validators() method in model class
        '''
        validators = TestModel.validators()
        assert len(validators) == 3, ('Wrong validator groups number: %s' %
                                      len(validators))
        names = sorted(utils.dict_keys(validators.keys()))
        assert names == sorted(TestModel._fields), ('Wrong validator groups '
                                                    'names: %s' % names)
        assert len(validators['test_type']) == 2, ('Wrong validators number '
                'for CharField with choices: %s' % validators['test_type'])
        assert len(validators['positive']) == 2, ('Wrong validators number '
                'for PositiveIntegerField: %s' % validators['positive'])
#        assert len(validators['name']) == 2, ('Wrong validators number '
#                'for uniquer char field: %s' % validators['name'])
#
#    def testUniqueField(self):
#        exists = TestModel(name="1", test_type='t', positive=1).save()
        


class ValidateTestCase(unittest.TestCase):
    '''Test case used to check validate function
    '''

    def testValidateFunction(self):
        '''Test validate function
        '''
        valids = {'field': [TrueFalseValidator()]}
        results = validators.validate(valids, {'field': True})
        assert results['field'] is True, ('Wrong validation results: %s' %
                                          results)
        results = validators.validate(valids, {'field': False})
        assert isinstance(results['field'], ErrorMonad), (
                'Wrong validation results: %s' % results)
        assert not results, 'Wrong validation results: %s' % repr(results)


def test():
    suite = unittest.TestSuite()
    suite.addTest(ValidatorClassTestCase('testSimpleValidator'))
    suite.addTest(ValidatorClassTestCase('testCustomErrorMessage'))
    suite.addTest(ValidatorsTestCase('testChoicesValidator'))
    suite.addTest(ModelValidatorsTestCase('testModelValidator'))
    suite.addTest(ValidateTestCase('testValidateFunction'))
    return suite
