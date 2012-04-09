Lighty-template
===============

Lighty-template is very simple template engine for python (python.org). 
Template syntax looks like django-template or jinja2 template. But template 
engine code is easier and gives a way to write all needed tags without any 
hacks. 

Now it does not include all features django-template or jinja2 supports, but 
I'll try to fix it as soon as possible.

Features:
---------

- Stupid simple syntax almost compatible with django-template.
- Pure python.
- Supports both Python 2 (checked with 2.7.2) and Python 3 (checked with 3.2.2)
- Fast. From 3 to 10 times faster than django-template and even faster on some
  benchmarks than jinja2 (but in one benchmark 2 times slower).
- Simple and compact code.
- Template filters with multiply arguments.
- Basic template filters included (now just 14 template filters).
- Basic template tags included.
- Simple but powerfull tag declaration - it's easy to create your own block 
  tags with writing single function.
- Custom template tags can modify template on fly.

Example:
--------

	<!DOCTYPE html>
	<html>
	<head>
		<title>{{ title }}</title>
		{% block style %}{% endblock %}
		{% block script %}{% endblock %}
	</head>
	<body>
		{% block content %}
		<h1>Hello, world!</h1>
		<p>Some text here</p>
		{% endblock %}
	</body>
	</html>

TODO:
-----

- More default tags (now there is no load, include tags, and if and for tags
  was simplified)
- More default filters (date formatiing, strings saving, etc.)
- Some additional execution optimizations.
- More tests (in progress).
- Documentation.
=======

Lighty-DB
=========

This is simple Python ORM that can be used now just with MongoDB. But I think 
in nearest future it would also support another backends. It looks almost like
Django's ORM but has a few differences.


Data model definition
---------------------

To work with data at first you must to define a model class that represents
database entity structure. For this purpose you can use lighty.db.models.Model
class and Field's subclasses from lighty.db.fields package. As example we create
a simple User entity with name, password and age.

	from lighty.db import fields, models

	class User(models.Model):
		name = fields.CharField()
		pass = fields.EmailField()
		age  = fields.IntegerField()

		def __str__(self):
			return "%s %d" % (self.name, self.age)

This class can be easy mapped from database and into database. As example to
store the data we need just:

	User(name='Peter', pass='secret_phrase', age=18).put()

or for step by step properties setting:

	john		= User()
	john.name	= 'John'
	john.age	= 19
	john.pass	= 'remomber me'
	john.save()

save() method is just an alias for put().

To get single entity from database by you can use get() method with name of the
fields and their values to identify the record:

	fred = User.get(name='fred', age=17)

To delete the entity from database you can use python del operator:

	del fred

Selecting the data from database
--------------------------------

As you can see from previous examples, there is no managers for data accessing.
For selection few records from database you can use queries to describe your
requirements to items be selected. To get all the users from database you can
use all() method of lighty.db.models.Model:

	for user in User.all():
		print user

To delete all the users from database you can use delete() method:

	User.delete()

But let's back to queries. To make a query it's easy to use pure Python syntax.
There is not suffixes for name arguments like it was in Django. You just need to
use model's fields and python operators to make a queries.

	User.all().where(User.age > 17)

selects all the users with age higher than 17. Or more complex example:

	User.all().where((User.age > 17) & (User.name == 'Peter'))

selects all the users with age higher that 17 and name equals to 'Peter'. For
now you can use:

- >, >=, <, <=, ==, &, |, +, - operators for all the values, 
- +, -, /, *, ** operators for mathematical fields
- slices for sequence fields (like a strings)

Also queries supports ordering:

	User.all().order_by(User.age): 

and slicing:

	User.all()[0:10] # Select first 10 user

You can also make operations with queries:

	query = User.all().where(User.age > 17) & User.all().where(User.age <= 20)

with results equivalent to:

	query = User.all().where((User.age > 17) & (User.age <= 20))

All the queries are lazy and it would be just one request to database when you
would like to fetch the data from database or iterate over query:

	User.all().where((User.age > 17) & (User.age <= 20)).fetch()

But do not forget - now there is no caching for query results and multiply 
fetching or iterations requires multiply requests to database. I would add
optional query caching in future.

You can also delete query results:

	User.all().delete() # Delete all the user entities

Or update this data:

	User.all().where(User.age < 18).update(age=18)


TODO
----

It' a lot of the things left to be added or improved.

- Make all the features described workable.
- Add a query results caching.
- Write more tests.
- Write more detailed documentation.
- Add mutiply backends support.
- Add SQLite, PostgreSQL and MySQL support.
- Add another NoSQL databases support.
- Add list and dict model fields
- Add foreign keys and many to many relations.
- Play with perfomance.
