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
        def execute_tag(context):
            return tag_manager.execute(name, token, context, block, 
                                        self, self.loader)
        return execute_tag

    def parse(self, text):
        """ Parse template string and create appropriate command list into this
        template instance """
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

    def exec_cmd(self, context):
        for command in self.commands:
            yield command(context)

    def execute(self, context):
        result = StringIO.StringIO()
        for cmd in self.exec_cmd(context):
            result.write(cmd)
        return result.getvalue()
