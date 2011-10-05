from lighty.db import fields, models, backend

class User(models.Model):
    name = fields.CharField()
    age  = fields.IntegerField()

backend.datastore.db.User.drop()

User(name='Peter', age=18).save()
User(name='John', age=19).save()
User(name='Harry', age=17).save()

for user in User.all():
    print user
