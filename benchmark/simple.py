import timeit
from helpers import print_time

template = '"Hello {{ name }}!"'
print '\n', template, '\n'

print_time('linja2', timeit.repeat("template.render(name='John Doe')",
            "from jinja2 import Template; template = Template(%s)" % template,
            repeat=5, number=10000))

print_time('lighty', timeit.repeat("template.execute({'name': 'John Doe'})",
            "from lighty.templates import Template; template = Template();" +
            "template.parse(%s)" % template, repeat=5, number=10000))

print_time('django', timeit.repeat("template.render(context)",
    "import djangohelper; from django.template import Context, " +
    "Template; template = Template(%s); " % template +
    "context = Context({'name': 'John Doe'})", repeat=5, number=10000))
