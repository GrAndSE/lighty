from lighty.db import fields, models, query

class User(models.Model):
    name = fields.CharField()
    age  = fields.IntegerField()
    objects = query.Query

for user in User.objects():
    print user
