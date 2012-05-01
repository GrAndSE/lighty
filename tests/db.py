'''Test case for MongoDB database backend
'''
import unittest

from lighty.db import fields, models


class ModelTestCase(unittest.TestCase):
    '''Test case
    '''

    def testClassExtending(self):
        '''Test is child class inherit all the field from parent class
        '''
        class Base(models.Model):
            title = fields.CharField()

        class Child(Base):
            text = fields.TextField()

        assert 'title' in Child._fields, (
                        'Error on model class extending: %s' % Child._fields)
        assert isinstance(Child.title, fields.CharField), (
                        'Error on model class extending: %s' % Child.title)


def test():
    suite = unittest.TestSuite()
    suite.addTest(ModelTestCase('testClassExtending'))
    return suite
