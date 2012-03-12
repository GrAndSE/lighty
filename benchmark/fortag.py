import timeit
from helpers import print_time

template = '''"""<!DOCTYPE html>
<html>
<head>
    <title>For test page</title>
</head>
<body>
    <ul>
    {% for i in items %}
        <li>{{ i }}</li>
    {% endfor %}
    </ul>
</body>
</html>"""'''
print '\n', template, '\n'

print_time('linja2', timeit.repeat(
           "template.render(items=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0])",
           "from jinja2 import Template; template = Template(%s)" % template,
           repeat=5, number=10000))

print_time('lighty', timeit.repeat(
           "template.execute({'items': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]})",
           "from lighty.templates import Template; template = Template();" +
           "template.parse(%s)" % template, repeat=5, number=10000))

print_time('django', timeit.repeat("template.render(context)",
    "import djangohelper; from django.template import Context, Template; " +
    "template = Template(%s); " % template +
    "context = Context({'items': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]})",
    repeat=5, number=10000))
