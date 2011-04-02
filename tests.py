base = """<!DOCTYPE html>
<html>
<head>
  <title>{{ title }}</title>
  {% block head %}{% endblock %}
</head>
<body>
  {% block content %}{% endbock %}
</body>
</html>"""
extended = """{% extend "base.html" %}
{% block head %}<style></style>{% endblock %}
{% block content %}<h1>Hello, world!</h1>{% endblock %}"""


from lighty.templates import Template

base_template = Template()
base_template.parse(base)
print(base_template.commands)
print(base_template.execute({'title': 'Hello'}))
extend_template = Template()
extend_template.parse(extended)
print(extend_template.commands)
print(extend_template.execute({'title': 'Hello'}))
