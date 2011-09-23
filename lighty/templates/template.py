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
from filter import filter_manager
from tag import tag_manager, parse_token


class Template(object):
    """Class represents template
    """
    TEXT    = 1
    TOKEN   = 2
    ECHO    = 3
    FILTER  = 4
    TAG     = 5
    STRING  = 6
    CLOSE   = 7

    def __init__(self, loader=TemplateLoader(), name="unnamed"):
        """Create new template instance
        """
        super(Template, self).__init__()
        self.loader = loader
        self.loader.register(name, self)
        self.commands = []
        self.context = {}

    @staticmethod
    def get_field(obj, field):
        if hasattr(obj, field):
            return getattr(obj, field)
        elif hasattr(obj, '__getitem__') and hasattr(obj, '__contains__'):
            return obj[field]
        raise Exception, 'Could not get %s from %s' % (field, obj)

    @staticmethod
    def variable(name):
        fields = name.split('.')
        if len(fields) > 1:
            def print_value(context):
                fields[0] = context[fields[0]]
                return reduce(Template.get_field, fields)
        else:
            def print_value(context): 
                return context[name]
        return print_value

    @staticmethod
    def constant(value):
        def print_constant(context):
            return value
        return print_constant

    @staticmethod
    def filter(value):
        '''Parse the tamplte filter
        '''
        parts   = value.split('|')
        variable= parts[0]
        filters = []
        for token in parts[1:]:
            if ':' in token:
                parsed = token.split(':')
                if len(parsed) > 1:
                    filter, args_token = parsed
                    args, types = parse_token(args_token)
                else:
                    filter      = parsed
                    args, types = (), ()
            else:
                filter = token
                args, types = (), ()
            filters.append((filter, args, types))
        def apply_filters(context):
            def apply_filter(value, pair):
                filter, args, types = pair
                return filter_manager.apply(filter, value, args, types, context)
            if variable[0] == '"' or variable[0] == "'":
                if variable[0] == variable[-1]:
                    filters.insert(0, variable[1:-1])
                else:
                    raise Exception('Template filter syntax error')
            else:
                filters.insert(0, Template.variable(variable)(context))
            return str(reduce(apply_filter, filters))
        return apply_filters
        
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
            elif current == Template.ECHO or current == Template.FILTER:
                if char == '}':
                    if len(token) > 0:
                        token = token.strip()
                        if current == Template.ECHO:
                            cmd = Template.variable(token)
                        else:
                            cmd = Template.filter(token)
                        cmds.append(cmd)
                        token = ''
                    current = Template.CLOSE
                elif char == '|':
                    current = Template.FILTER
                    token += str(char)
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
        # Last value
        if len(token) > 0:
            cmds.append(Template.constant(token))
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
