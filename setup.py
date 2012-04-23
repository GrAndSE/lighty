#!/usr/bin/env python
"""
Lighty
~~~~~~

Lighty is a simple all-in-one web framework writen in Python.
"""
from distutils.core import setup

setup(
        name='lighty',
        version='0.4.1',
        description='Simple all-in-one web framework',
        long_description=__doc__,
        keywords='Template HTML XML', 
        author='Andrey Grygoryev',
        author_email='undeadgrandse@gmail.com',
        license='BSD',
        url='https://github.com/GrAndSE/lighty',
        packages=['lighty', 'lighty.db', 'lighty.templates', 'lighty.wsgi'],
        platforms="any",
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing :: Markup :: HTML',
            'Topic :: WSGI'
        ],
)
