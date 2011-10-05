from lighty.db import fields, models, query, backend

class User(models.Model):
    name = fields.CharField()
    age  = fields.IntegerField()
    objects = query.Query

print backend.datastore.db.User.drop()

User(name='Peter', age=18).save()
User(name='John', age=19).save()
User(name='Harry', age=17).save()

for user in User.objects():
    print user
