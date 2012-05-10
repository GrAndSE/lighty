'''
This is simple Python ORM that can be used now just with MongoDB. But I think
in nearest future it would also support another backends. It looks almost like
Django's ORM but has a few differences.

Data model definition
---------------------

To work with data at first you must to define a model class that represents
database entity structure. For this purpose you can use lighty.db.models.Model
class and Field's subclasses from lighty.db.fields package. As example we
create simple User entity with name, password and age::

    from lighty.db import fields, models

    class User(models.Model):
        name = fields.CharField()
        pass = fields.EmailField()
        age = fields.IntegerField()

        def __str__(self):
            return "%s %d" % (self.name, self.age)

This class can be easy mapped from database and into database. As example to
store the data we need just:::

    User(name='Peter', pass='secret_phrase', age=18).put()

or for step by step properties setting::

    john = User()
    john.name = 'John'
    john.age = 19
    john.pass = 'remomber me'
    john.save()

save() method is just an alias for put().

To get single entity from database by you can use get() method with name of the
fields and their values to identify the record:::

    fred = User.get(name='fred', age=17)

To delete the entity from database you can use delete() method::

    fred.delete()

Selecting the data from database
--------------------------------

As you can see from previous examples, there is no managers for data accessing.
For selection few records from database you can use queries to describe your
requirements to items be selected. To get all the users from database you can
use all() method of lighty.db.models.Model::

    for user in User.all():
        print user

To delete all the users from database you can use delete() method from Query::

    User.all().delete()

But let's back to queries. To make a query it's easy to use pure Python syntax.
There is not suffixes for name arguments like it was in Django. You just need
to use model's fields and python operators to make a queries.::

    User.all().where(User.age > 17)

selects all the users with age higher than 17. Or more complex example::

    User.all().where((User.age > 17) & (User.name == 'Peter'))

selects all the users with age higher that 17 and name equals to 'Peter'. For
now you can use:

- `>`, `>=`, `<`, `<=`, `==`, `&`, `|` and `+` operators for all the values
- `+`, `-`, `/`, `*` and `**` operators for mathematical fields
- slices for sequence fields (like a strings)

Also queries supports ordering::

    User.all().order_by(User.age)

and slicing::

    User.all()[0:10] # Select first 10 user

You can also make operations with queries::

    query = User.all().where(User.age > 17) & User.all().where(User.age <= 20)

with results equivalent to::

    query = User.all().where((User.age > 17) & (User.age <= 20))

All the queries are lazy and it would be just one request to database when you
would like to fetch the data from database or iterate over query::

    User.all().where((User.age > 17) & (User.age <= 20)).fetch()

But do not forget - now there is no caching for query results and multiply
fetching or iterations requires multiply requests to database. If you would
like to add caching you can use fetch method with argument cache set to True::

    User.all().where((User.age > 17) & (User.age <= 20)).fetch(cache=True)

After that all other iterations over this query or len() function will work
with cache. But cacheng uses additional memory and may work with outdated data.

Also you can update data for query::

    User.all().where(User.age < 18).update(age=18)
'''
from .backend import manager


def init_db_manager(settings):
    '''Get database connections from settings
    '''
    for section in settings.sections():
        if section.startswith('DATABASE:'):
            name = section.replace('DATABASE:', '')
            args = settings.section(section)
            manager.connect(name, **args)

