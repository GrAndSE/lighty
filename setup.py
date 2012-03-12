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

- Stupid simple syntax almost compatible with django-template
- Pure python
- Fast. Looks ten times faster than django-template and four times faster than
  jinja2 on some cases and two times slower on another cases.
- Simple and compact code
- Template filters with multiply arguments
- Basic template filters included (now just 14 template filters)
- Simple but powerfull tag declaration - it's easy to create your own block 
  tags with writing single function
- Custom template tags can modify template on fly

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
		<h1>Hello, world!</h1>
		<p>Some text here</p>
		{% endblock %}
	</body>
	</html>

TODO:
-----

- More default tags and additional funcctions for tags exists (now there is 
  no additional logic for if tag and no with and load tags)
- More default filters (date formatiing, strings saving, etc.)
- Some execution optimizations
- More tests (in progress) and benchmarks
- Documentation
"""
from setuptools import setup, find_packages

setup(
        name='lighty-template',
        version='0.3.0',
        description='Simple template engine for python',
        long_description=open('README').read(),
        keywords='Template HTML XML', 
        author='Andrey Grygoryev',
        author_email='undeadgrandse@gmail.com',
        license='BSD',
        url='https://github.com/GrAndSE/lighty-template',
        packages=find_packages(),
        platforms="any",
        zip_safe=False,
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing :: Markup :: HTML',
        ],
)
