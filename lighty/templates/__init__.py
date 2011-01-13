""" Pakage provides method to working with templates """

try:
    import cStringIO as StringIO
except:
    try:
        import StringIO
    except:
        import io as StringIO

from loaders import TemplateLoader


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
        self.loader.register(name, self)
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
        """ Parse template string and create appropriate command list into this
        template instance """
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


