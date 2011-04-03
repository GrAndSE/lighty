from lighty.templates.tag import parse_token

assert ['test.html'] == parse_token('"test.html"'),\
        'Remove brackets failed: %s' % parse_token('"test.html"')
assert ['test\'html'] == parse_token('"test\'html"'),\
        'Remove brackets from sentence with inner brackets failed: %s' %\
        parse_token('"test\'html"')
assert ['a', 'in', 'b'] == parse_token('a in b'),\
        'Simple token parsing failed: %s' % parse_token('a in b')
assert ['a', 'as', 'Let me in'] == parse_token('a as "Let me in"'),\
        'Token with sentence parse failed: %s' %\
        parse_token('a as "Let me in"')

base = """<!DOCTYPE html>
<html>
<head>
  <title>{{ title }}</title>
  {% block head %}{% endblock %}
</head>
<body>
  {% block content %}Some contents{% endblock %}
</body>
</html>"""
extended = """{% extend "base.html" %}
{% block head %}<style></style>{% endblock %}
{% block content %}<h1>Hello, world!</h1>{% endblock %}"""


from lighty.templates import Template

base_template = Template(name='base.html')
base_template.parse(base)
print(base_template.commands)
print(base_template.execute({'title': 'Hello'}))
extend_template = Template(loader=base_template.loader)
extend_template.parse(extended)
print(extend_template.commands)
print(extend_template.execute({'title': 'Hello'}))
