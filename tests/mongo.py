'''Test case for MongoDB database backend
'''
import unittest

from lighty.db import fields, models, backend


class User(models.Model):
    name = fields.CharField()
    age = fields.IntegerField()

    def __str__(self):
        return "%s %d" % (self.name, self.age)


class MongoTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        backend.datastore.db.User.drop()

        User(name='Peter', age=18).save()
        User(name='John', age=19).save()
        User(name='Harry', age=17).save()

    def testCreate(self):
        user = User(name='Harry', age=20)
        assert not user._is_saved, 'Model saved on creation'
        user.save()
        assert user._is_saved, 'Model _is_saved not changes after was saved'
        assert user.key(), 'Model key error after object was saved'

    def testGetAll(self):
        '''Test Model.all() method
        '''
        users = [user for user in User.all()]
        assert (users[0].name == 'Peter' and users[1].name == 'John' and 
                 users[2].name == 'Harry'), ('Wrong result [%s]' %
                         ','.join([str(user) for user in users]))
        assert (users[0].age == 18 and users[1].age == 19 and 
                 users[2].age == 17), ('Wrong result [%s]' % 
                         ','.join([str(user) for user in users]))

    def testCount(self):
        '''Test len(query) method
        '''
        users = [user for user in User.all()]
        assert len(users) == len(User.all()), ('Wrong number of items: '
                '%d != %d' % (len(users), len(User.all())))
        query = User.all().where((User.age > 17) & (User.name == 'Peter'))
        users = [user for user in query]
        assert len(users) == len(query), 'Wrong number of items: %d != %s' % (
                len(users) == len(query))

    def testOrder(self):
        '''Test query ordering
        '''
        users = [user for user in User.all().order_by(User.age)]
        assert (users[0].age == 17 and users[1].age == 18 and 
                 users[2].age == 19), ('Wrong result [%s]' % 
                         ','.join([str(user) for user in users]))

    def testSimple(self):
        '''Test simple query
        '''
        users = [user for user in User.all().where(User.age > 17)]
        assert users[0].age == 18 and users[1].age == 19, (
                'Wrong result [%s]' % ','.join([str(user) for user in users]))

    def testQuery(self):
        '''Test queries with some logic
        '''
        users = [user for user in User.all().where((User.age > 17) &
                                                   (User.name == 'Peter'))]
        assert users[0].name == 'Peter' and users[0].age == 18, (
                 'Wrong result [%s]' % ','.join([str(user) for user in users]))

    def testGet(self):
        '''Test Model.get() method
        '''
        user = User.get(name='Peter')
        assert user, 'Wrong result searching for name: %s' % user
        assert user.name == 'Peter', ('Wrong result searching for name: %s' %
                                      user)
        assert user.age == 18, 'Wrong result searching for name: %s' % user
        user = User.get(name='John', age=19)
        assert user, 'Wrong result searching for two fields: %s' % user
        assert user.name == 'John', ('Wrong result searching for name: %s' %
                                     user)
        assert user.age == 19, 'Wrong result searching for name: %s' % user
        user = User.get(name='adad')
        assert not user, 'Wrong not found result: %s' % user
        assert not user.name, 'Wrong not found result: %s' % user

    def testDelete(self):
        '''Test entity.delete() method
        '''
        User.get(name='Peter').delete()
        assert len(User.all().where(User.name == 'Peter')) == 0, (
                'Error deleting entity')
        assert len(User.all()) == 2, 'Error deleting entity'

    def testChange(self):
        '''Test save changes into entity
        '''
        user = User.get(name='Peter')
        user.name = 'Alex'
        user.save()
        assert len(User.all().where(User.name == 'Alex')) == 1, (
                'Error saving entity')
        assert len(User.all().where(User.name == 'Peter')) == 0, (
                'Error saving entity')


def test():
    suite = unittest.TestSuite()
    suite.addTest(MongoTestCase('testCreate'))
    suite.addTest(MongoTestCase('testGet'))
    suite.addTest(MongoTestCase('testGetAll'))
    suite.addTest(MongoTestCase('testChange'))
    suite.addTest(MongoTestCase('testOrder'))
    suite.addTest(MongoTestCase('testSimple'))
    suite.addTest(MongoTestCase('testQuery'))
    suite.addTest(MongoTestCase('testCount'))
    suite.addTest(MongoTestCase('testDelete'))
    return suite
