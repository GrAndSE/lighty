'''Test case for MongoDB database backend
'''
import unittest

from lighty.db import fields, models, backend

backend.manager.connect('default')


class User(models.Model):
    name = fields.CharField()
    age = fields.IntegerField()
    created = fields.DateField(auto_now_add=True)
    changed = fields.DateTimeField(auto_now=True)
    birthday = fields.DateField(null=True)

    def __str__(self):
        return "%s %d" % (self.name, self.age)


def datetime_equals(first, second):
    return (first.year == second.year and first.month == second.month and
            first.day == second.day and first.hour == second.hour and
            first.minute == second.minute and first.second == second.second)


class MongoTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''
    def setUp(self):
        backend.manager.default.db.User.drop()

        User(name='Peter', age=18).save()
        User(name='John', age=19).save()
        User(name='Harry', age=17).save()

    def testCreate(self):
        '''Test model creation method
        '''
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

    def testGetByKey(self):
        '''Test Model.get(object_key) method
        '''
        key = User(name='Kevin', age=20).save().key()
        user = User.get(key)
        assert user, 'Wrong result getting entity for key: %s' % user
        assert user.name == 'Kevin', ('Wrong result getting entity name for '
                                      'key: %s' % user.name)
        assert user.age == 20, ('Wrong result getting entity name for '
                                'key: %s' % user.age)

    def testGet(self):
        '''Test Model.get(field_name=value) method
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

    def testDateTime(self):
        '''Test different date/time fields
        '''
        # This method so big becouse it requires to take some time to execute
        # to check change time properly, exceptially in queries
        from datetime import date, datetime, timedelta
        now = datetime.now()
        today = date.today()
        birthday = birthday=today - timedelta(days=20*366)
        user = User(name='Kevin', age=20, birthday=birthday).save()
        changed = user.changed
        # Check auto filled dates
        assert user.birthday == birthday, ('Manually setted value error: %s'
                                   ' except %s' % (user.birthday, birthday))
        assert user.created == today, ('auto_now_add value error: %s except '
                                       '%s' % (user.created, today))
        assert datetime_equals(user.changed, now), ('auto_now value error: %s'
                                        ' except %s' % (user.changed, now))
        # Test few queries with date objects
        selected = User.all().where(User.created <= today)
        assert len(selected) == 4, ('Wrong date query results number: %s' %
                                    len(selected))
        user.created = today + timedelta(days=2)
        user.save()
        selected = User.all().where(User.created > today)
        assert len(selected) == 1, ('Wrong date query results number: %s' %
                                    len(selected))
        # Update user, save and check changed time
        user.name = 'Kevin'
        user.save()
        assert user.changed > changed, 'Error changed auto_now: %s' % changed
        # Check queries
        updated = User.all().where(User.changed > changed)
        assert len(updated) == 1, ('Wrong query results number: %s' %
                                   len(updated))
        assert updated[0].name == 'Kevin', ('Wrong result item: %s' %
                                            updated[0].name)


def test():
    suite = unittest.TestSuite()
    suite.addTest(MongoTestCase('testCreate'))
    suite.addTest(MongoTestCase('testGet'))
    suite.addTest(MongoTestCase('testGetByKey'))
    suite.addTest(MongoTestCase('testGetAll'))
    suite.addTest(MongoTestCase('testChange'))
    suite.addTest(MongoTestCase('testOrder'))
    suite.addTest(MongoTestCase('testSimple'))
    suite.addTest(MongoTestCase('testQuery'))
    suite.addTest(MongoTestCase('testCount'))
    suite.addTest(MongoTestCase('testDelete'))
    suite.addTest(MongoTestCase('testDateTime'))
    return suite
