#!/usr/bin/env python
"""
Lighty
======

Lighty is a simple all in one web framework writen in Python. It includes:

- Tool to configure applications using configuration files.
- Simple ORM to access MongoDB (other databases will be added in future). This
  ORM looks close to Django's ORM.
- Simple but powerfull and fast template engine almost like Django Templates or
  Jinja2.
- URL routing: can easy resolve urls described in specified format and reverse
  urls for view name and arguments taken.
- Bindings to WSGI and Tornado.

It's not a full list of features. To read more look into documentation.
"""
from distutils.core import setup

setup(
    name='lighty',
    version='0.4.3',
    description='Simple all-in-one web framework',
    long_description=__doc__,
    keywords='Template HTML XML', 
    author='Andrey Grygoryev',
    author_email='undeadgrandse@gmail.com',
    license='BSD',
    url='https://github.com/GrAndSE/lighty',
    packages=['lighty', 'lighty.db', 'lighty.templates', 'lighty.wsgi'],
    data_files=[('lighty/wsgi/templates',
                 ['lighty/wsgi/templates/debug.html'])],
    platforms="any",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',       
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
