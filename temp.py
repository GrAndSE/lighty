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


class TagManager(object):
    """ Class used for tags manipulation """

    def __init__(self):
        """ Create new tag managet instance """
        super(TagManager, self).__init__()
        self.tags = {}

    def register(self, name, tag, block_tag=False, context_required=False,
                 template_required=False, loader_required=False):
        """ Register new tag """
        self.tags[name] = (
            tag,
            block_tag,
            context_requiered,
            template_required,
            loader_required
        )

    def execute(self, name, token, context, block, template, loader):
        """ Execute tag """
        if name not in self.tags:
            raise Exception("Tag '%s' is not registered" % name)
        tag = self.tags
        args = {
            'token': token
        }
        if tag[1]: args['block'] = block
        if tag[2]: args['context'] = context
        if tag[3]: args['template'] = template
        if tag[4]: args['loader'] = loader
        return tag[0](**args)


class TemplateLoader(object):
    """ Class fot managing templates """

    def __init__(self, settings=None):
        """ Create new template loader """
        super(TemplateLoader, self).__init__()
        # Create new templates dictionary
        self.templates = {}
        # TODO: do something with settings


    def add_template(self, name, template):
        """ Add loaded or generated template """
        self.templates[name] = template

    def get_template(self, name):
        """ Get template by name """
        if name not in self.templates:
            raise Exception("Template '%s' was not found" % name)
        return self.templates[name]


try:
    import cStringIO as StringIO
except:
    try:
        import StringIO
    except:
        import io as StringIO


class Template(object):
    """ Class represents template """

    TEXT    = 1
    TOKEN   = 2
    ECHO    = 3
    TAG     = 4
    STRING  = 5
    CLOSE   = 6

    def __init__(self, loader=TemplateLoader(), name="unnamed"):
        """ Create new template instance """
        super(Template, self).__init__()
        self.loader = loader
        self.loader.add_template(name, self)
        self.commands = []


    @staticmethod
    def variable(name):
        def print_value(context):
            return context[name]
        return print_value

    @staticmethod
    def constant(value):
        def print_value(context):
            return value
        return print_value

    def parse(self, text):
        current = Template.TEXT
        token   = ''
        for char in text:
            if current == Template.TEXT:
                if char == '{':
                    current = Template.TOKEN
                    if len(token) > 0:
                        self.commands.append(Template.constant(token))
                        token = ''
                else:
                    token += str(char)
            elif current == Template.TOKEN:
                if char == '{':
                    current = Template.ECHO
                elif char == '%':
                    current = Template.TAG
                else:
                    current = Template.TEXT
                    token = '{'+str(char)
            elif current == Template.ECHO:
                if char == '}':
                    current = Template.CLOSE
                    if len(token) > 0:
                        self.commands.append(Template.variable(token.strip()))
                        token = ''
                else:
                    token += str(char)
            elif current == Template.TAG:
                if char == '%':
                    current = Template.CLOSE
                    token = ''
                else:
                    token += str(char)
            elif current == Template.CLOSE:
                if char == '}':
                    current = Template.TEXT
                else:
                    raise Exception('Wrong template syntax')
            else:
                raise Exception('Wrong template syntax')

    def exec_cmd(self, context):
        for command in self.commands:
            yield command(context)

    def execute(self, context):
        result = StringIO.StringIO()
        for cmd in self.exec_cmd(context):
            result.write(cmd)
        return result.getvalue()

base_template = Template()
base_template.parse(base)
print(base_template.commands)
print(base_template.execute({'title': 'Hello'}))
