import timeit
from helpers import print_time

if_template = '''"""<!DOCTYPE html>
<html>
<head>
    <title>If test page</title>
</head>
<body>
    {% if user %}
        <h1>Hello {{ user.name }}!</h1>
        {% if user.is_authenticated %}
            <h2>Wellcome back</h2>
        {% endif %}
    {% endif %}
</body>
</html>"""'''
print '\n', if_template, '\n'

print_time('linja2', timeit.repeat(
        "template.render(user={'name':'John Doe', 'is_authenticated':False})",
        "from jinja2 import Template; template = Template(%s)" % if_template,
        repeat=5, number=10000))

print_time('lighty', timeit.repeat(
            "template.execute({'user': {'name': 'John Doe', " +
            "'is_authenticated': False}})",
            "from lighty.templates import Template; template = Template();" +
            "template.parse(%s)" % if_template, repeat=5, number=10000))

print_time('django', timeit.repeat("template.render(context)",
    "import djangohelper; from django.template import Context, Template; " +
    "template = Template(%s); " % if_template +
    "context = Context({'user':{'name':'John Doe','is_authenticated':False}})",
    repeat=5, number=10000))
