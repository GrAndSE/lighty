"""Lighty-template is very simple template engine for python (python.org). 
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

Simple template example (let's call it index.html):

.. code-block:: html

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

You can load you templates using templates loader. Usualy you need to use 
FSLoader class:::

    from lighty.templates.loaders import FSLoader

    loader = FSLoader(['tests/templates'])
    template = loader.get_template('index.html')

Above code means that we create new FSLoader that discover templates in path
'tests/templates'. If we place our 'index.html' template into this path this
code can works fine and we can render template with some context:::

    result = template.execute({'title': 'Page title'})

or just::

    result = template({'title': 'Page title'})

Note that if there is no variable 'title' specified in context template raises
exception. Lighty-template is strict template engine requires to be carefull
with your templates and variables in context for rendering. I think that
usually strict means better and safe.
"""

from .loaders import TemplateLoader as Loader
from .template import Template as BaseTemplate

from .templatetags import *

TemplateLoader = Loader
Template = BaseTemplate
