#!/usr/bin/env python
"""
Lighty-template
~~~~~~~~~~~~~~~

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

Here a small template example:

	<!DOCTYPE html>
	<html>
	<head>
		<title>{{ title }}</title>
		{% block style %}{% endblock %}
		{% block script %}{% endblock %}
	</head>
	<body>
		{% block content %}
		<h1>Hello, {{ name }}!</h1>
		<p>Some text here</p>
		{% endblock %}
		{% include "includes/footer.html" %}
	</body>
	</html>

TODO:
-----

- More default tags (now there is no load tags, and if and for tags was
  simplified and requires additional work).
- More default filters (date formatiing, strings saving, etc.)
- Some additional execution optimizations.
- More tests (in progress).
- Documentation.
- Thinking about unicode and escaping.
"""
from distutils.core import setup

setup(
        name='lighty-template',
        version='0.3.3',
        description='Simple template engine for python',
        long_description=__doc__,
        keywords='Template HTML XML', 
        author='Andrey Grygoryev',
        author_email='undeadgrandse@gmail.com',
        license='BSD',
        url='https://github.com/GrAndSE/lighty-template',
        packages=['lighty', 'lighty.templates'],
        platforms="any",
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing :: Markup :: HTML',
        ],
)
