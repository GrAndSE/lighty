from lighty.db import fields, models, backend

class User(models.Model):
    name = fields.CharField()
    age  = fields.IntegerField()

    def __str__(self):
        return "%s %d" % (self.name, self.age)

backend.datastore.db.User.drop()

User(name='Peter', age=18).save()
User(name='John', age=19).save()
User(name='Harry', age=17).save()

for user in User.all():
    print user
print ''

for user in User.all().order_by(User.age):
    print user
print ''

for user in User.all().where(User.age > 17):
    print user
print ''

for user in User.all().where((User.age > 17) & (User.name == 'Peter')):
    print user
print ''
