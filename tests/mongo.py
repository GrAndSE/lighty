'''Test case for whole template
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

    def testGetAll(self):
        users = [user for user in User.all()]
        assert (users[0].name == 'Peter' and users[1].name == 'John' and 
                 users[2].name == 'Harry'), ('Wrong result [%s]' %
                         ','.join([str(user) for user in users]))
        assert (users[0].age == 18 and users[1].age == 19 and 
                 users[2].age == 17), ('Wrong result [%s]' % 
                         ','.join([str(user) for user in users]))

    def testOrder(self):
        users = [user for user in User.all().order_by(User.age)]
        assert (users[0].age == 17 and users[1].age == 18 and 
                 users[2].age == 19), ('Wrong result [%s]' % 
                         ','.join([str(user) for user in users]))

    def testSimple(self):
        users = [user for user in User.all().where(User.age > 17)]
        assert users[0].age == 18 and users[1].age == 19, (
                'Wrong result [%s]' % ','.join([str(user) for user in users]))

    def testQuery(self):
        users = [user for user in User.all().where((User.age > 17) &
                                                   (User.name == 'Peter'))]
        assert users[0].name == 'Peter' and users[0].age == 18, (
                 'Wrong result [%s]' % ','.join([str(user) for user in users]))

    def testGet(self):
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


def test():
    suite = unittest.TestSuite()
    suite.addTest(MongoTestCase('testGet'))
    suite.addTest(MongoTestCase('testGetAll'))
    suite.addTest(MongoTestCase('testOrder'))
    suite.addTest(MongoTestCase('testSimple'))
    suite.addTest(MongoTestCase('testQuery'))
    return suite
