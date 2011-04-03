""" Package provides template class """

from collections import deque
try:
    import cStringIO as StringIO
except:
#    try:
#        import StringIO
#    except:
#        import io as StringIO
    pass


from loaders import TemplateLoader
from tag import tag_manager


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
        self.context = {}

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

    def tag(self, name, token, block):
        if tag_manager.is_lazy_tag(name):
            def execute_tag(context):
                return tag_manager.execute(name, token, context, block, 
                                           self, self.loader)
            return execute_tag
        else:
            result = tag_manager.execute(name, token, self.context, block, 
                                         self, self.loader)
            if callable(result):
                return result
            else:
                return lambda context: ''

    def parse(self, text):
        """Parse template string and create appropriate command list into this
        template instance 
        """
        current = Template.TEXT
        token   = ''
        cmds    = self.commands
        cmd_stack   = deque()
        tag_stack   = deque()
        token_stack = deque()
        for char in text:
            if current == Template.TEXT:
                if char == '{':
                    current = Template.TOKEN
                    if len(token) > 0:
                        cmds.append(Template.constant(token))
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
                        cmds.append(Template.variable(token.strip()))
                        token = ''
                else:
                    token += str(char)
            elif current == Template.TAG:
                if char == '%':
                    current = Template.CLOSE
                    token   = token.strip()
                    name    = token.split(' ', 1)[0]
                    if name.startswith('end'):
                        name    = name[3:]
                        tag     = tag_stack.pop()
                        # Close block
                        if name == tag:
                            block   = cmds
                            cmds    = cmd_stack.pop()
                            token   = token_stack.pop()
                            cmds.append(self.tag(name, token, block))
                        else:
                            raise Exception("Invalid closing tag: 'end%s' except 'end%s'" % (name, tag))
                    else:
                        if ' ' in token:
                            token = token.split(' ', 1)[1]
                        else:
                            token = ''
                        if tag_manager.is_block_tag(name):
                            cmd_stack.append(cmds)
                            tag_stack.append(name)
                            token_stack.append(token)
                            cmds = []
                        else:
                            cmds.append(self.tag(name, token, ()))
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
        # Check stack length - detect unclosed tags
        if len(cmd_stack) > 0:
            raise Exception('Unexpected end of input - not all tags closed')
        self.commands = cmds

    def execute(self, context):
        """Execute all commands on a specified context

        Arguments:
            context: dict contains varibles
        """
        result = StringIO.StringIO()
        for cmd in self.commands:
            result.write(cmd(context))
        return result.getvalue()

    def __call__(self, context):
        """Alias for execute()
        """
        return self.execute(context)
