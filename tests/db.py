'''Test case for MongoDB database backend
'''
import unittest

from lighty.db import backend, fields, models


class ModelTestCase(unittest.TestCase):
    '''Test case
    '''

    def testClassExtending(self):
        '''Test is child class inherit all the field from parent class
        '''
        class Base(models.Model):
            name = fields.CharField()

        class Child(Base):
            text = fields.TextField()

        assert 'name' in Child._fields, (
                        'Error on model class extending: %s' % Child._fields)
        assert isinstance(Child.name, fields.CharField), (
                        'Error on model class extending: %s' % Child.name)


class DatastoreTestCase(unittest.TestCase):
    '''Test case for datastore object
    '''
    class TestClass(models.Model):
        _datastore_name = 'test1'
        name = fields.CharField()

    def testBackendSwap(self):
        '''Test database swapping
        '''

        class TestClass(models.Model):
            _datastore_name = 'test2'
            name = fields.CharField()

        # Create and check objects
        DatastoreTestCase.TestClass(name='first').save()
        TestClass(name='second').save()
        first = DatastoreTestCase.TestClass.get(name='first')
        assert first, 'Error putting object into database: %s' % first
        second = TestClass.get(name='second')
        assert second, 'Error putting object into database: %s' % second
        # Swap databases and check again
        backend.manager.swap('test1', 'test2')
        first = DatastoreTestCase.TestClass.get(name='first')
        assert not first, 'Error swapping datastores: %s' % first
        second = TestClass.get(name='second')
        assert not second, 'Error swapping datastores: %s' % second
        first = DatastoreTestCase.TestClass.get(name='second')
        assert first, 'Error swapping datastores: %s' % first
        second = TestClass.get(name='first')
        assert second, 'Error swapping datastores: %s' % second
        # Swap datastores again. Now all must be fine
        backend.manager.swap('test1', 'test2')
        first = DatastoreTestCase.TestClass.get(name='first')
        assert first, 'Error putting object into database: %s' % first
        second = TestClass.get(name='second')
        assert second, 'Error putting object into database: %s' % second
        # Clean up
        for item in DatastoreTestCase.TestClass.all():
            item.delete()
        for item in TestClass.all():
            item.delete()


def test():
    suite = unittest.TestSuite()
    suite.addTest(ModelTestCase('testClassExtending'))
    suite.addTest(DatastoreTestCase('testBackendSwap'))
    return suite
