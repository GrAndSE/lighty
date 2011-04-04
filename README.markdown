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

- Stupid simple syntax almost compatible with django-template
- Pure python
- Simple and compact code
- Simple but powerfull tag declaration - it's easy to create your on block tags 
- Custom template tags can modify template on fly

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

- Filters
- Access to object fields
- Some execution optimizations
- More tests
= Documentation
