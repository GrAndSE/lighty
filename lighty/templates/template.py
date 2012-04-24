"""Module provides template two template classes:

- Template
- LazyTemplate
"""
from collections import deque
from functools import reduce
from decimal import Decimal
try:
    import cStringIO
    StringIO = cStringIO.StringIO
except:
    try:
        import StringIO as sio
        StringIO = sio.StringIO
    except:
        import io
        StringIO = io.StringIO

from .context import resolve
from .loaders import TemplateLoader
from .filter import filter_manager
from .tag import tag_manager, parse_token


class Template(object):
    """Class represents template. You can create template directrly in code::

        template = Template('<b>Hello, {{ name }}!</b>')

    or load it using template loader::

        template = loader.get_template('simple.html')

    Also you can create template and parse some text later but I do not
    recomend to do that:

        template = Template()
        template.parse({{ var }})

    To render the template you can use execute method and pass render context
    as single arguments to this methods:::

        template.execute({'var': 'test'})

    And you reciveve 'test' string as result of template execution. Or you can
    just call the template like a function to render template simpler way:::

        template({'var': 'test'})

    You can also access more complex variable in you context from templates, as
    example dict subclasses or even object fields:::

        >>> template = Template('Hello, {{ user.name }} from {{ var }}')
        >>> template({'user': {'name': 'Peter', 'is_authenticated': True},
        ...           'var': 'test'})
        'Hello, Peter from test'
    """
    TEXT = 1
    TOKEN = 2
    ECHO = 3
    FILTER = 4
    TAG = 5
    STRING = 6
    CLOSE = 7

    def __init__(self, text=None, loader=TemplateLoader(), name="unnamed"):
        """Create new template instance
        """
        super(Template, self).__init__()
        self.loader = loader
        self.name = name
        self.commands = []
        self.context = {}
        self.loader.register(name, self)
        if text is not None:
            self.parse(text)

    def __eq__(self, obj):
        return type(self) == type(obj) and self.name == obj.name

    @staticmethod
    def variable(name):
        def print_variable(context):
            return str(resolve(name, context))
        return print_variable

    @staticmethod
    def constant(value):
        def print_constant(context):
            return value
        return print_constant

    @staticmethod
    def filter(value):
        '''Parse the tamplte filter
        '''
        parts = value.split('|')
        filters = []
        variable = parts[0]
        for token in parts[1:]:
            if ':' in token:
                parsed = token.split(':')
                if len(parsed) > 1:
                    filter, args_token = parsed
                    args, types = parse_token(args_token)
                else:
                    filter = parsed
                    args, types = (), ()
            else:
                filter = token
                args, types = (), ()
            filters.append((filter, args, types))

        def apply_filters(context):
            def apply_filter(value, pair):
                filter, args, types = pair
                return filter_manager.apply(filter, value, args, types,
                                            context)
            if variable[0] == '"' or variable[0] == "'":
                if variable[0] == variable[-1]:
                    value_with_filters = [variable[1:-1]] + filters
                else:
                    raise Exception('Template filter syntax error')
            else:
                try:
                    value_with_filters = [Decimal(variable)] + filters
                except:
                    value_with_filters = [resolve(variable, context)] + filters
            return str(reduce(apply_filter, value_with_filters))
        return apply_filters

    def tag(self, name, token, block):
        if tag_manager.is_lazy_tag(name):
            def execute_tag(context):
                return tag_manager.execute(name, token, context, block, self,
                                           self.loader)
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
        token = ''
        cmds = self.commands
        cmd_stack = deque()
        tag_stack = deque()
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
                    token = '{' + str(char)
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
                    token = token.strip()
                    name = token.split(' ', 1)[0]
                    if name.startswith('end'):
                        name = name[3:]
                        tag = tag_stack.pop()
                        # Close block
                        if name == tag:
                            block = cmds
                            cmds = cmd_stack.pop()
                            token = token_stack.pop()
                            cmds.append(self.tag(name, token, block))
                        else:
                            raise Exception(
                                "Invalid closing tag: 'end%s' except 'end%s'" %
                                (name, tag))
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

    def execute(self, context={}):
        """Execute all commands on a specified context

        Arguments:
            context: dict contains varibles
        Returns:
            string contains the whole result
        """
        result = StringIO()
        for cmd in self.commands:
            result.write(cmd(context))
        value = result.getvalue()
        result.close()
        return value

    def __call__(self, context={}):
        """Alias for execute()
        """
        return self.execute(context)

    def partial(self, context, name='', key_args=()):
        """Execute all commands on a specified context and cache the result as
        another template ready for execution

        Arguments:
            context: dict contains variables
        Returns:
            another template contains the result
        """
        result = Template(loader=self.loader, name=name)
        buffer = StringIO()
        for cmd in self.commands:
            try:
                buffer.write(cmd(context))
            except Exception:
                value = buffer.getvalue()
                if len(value) > 0:
                    result.commands.append(Template.constant(value))
                result.commands.append(cmd)
                buffer.close()
                buffer = StringIO()
        value = buffer.getvalue()
        buffer.close()
        if len(value) > 0:
            result.commands.append(Template.constant(value))
        return result


class LazyTemplate(Template):
    '''Lazy template class change the way how template loaded. :class: Template
    parses template context on template creation if template text provided::

        >>> from lighty.templates.template import Template, LazyTemplate
        >>> template = Template('{{ var }}')  # template already parsed
        >>> template.commands
        [<function print_variable at 0xdda0c8>]
        >>> lazy = LazyTemplate('{{ var }}')  # not parsed
        >>> lazy.commands
        []
        >>> lazy.execute({'var': 'test'})  # parse on demand and then execute
        'test'
        >>> lazy.commands
        [<function print_variable at 0x1130140>]

    Lazy template class usefull for template loaders like a
    :class: lighty.templates.loader.FSLoader that requires to get the list of
    all the templates but does not require to parse all the templates on
    loading because it causes an error with templates loading order (when
    child template loaded before parent). Also it speed ups templates loading
    process because it does not require to parse all the templates when they
    even not used.
    '''

    def prepare(self):
        '''Prepare to execution
        '''
        self.parse = super(LazyTemplate, self).parse
        self.parse(self.text)
        del self.text
        execute = super(LazyTemplate, self).execute
        self.execute = execute
        return execute

    def parse(self, text):
        '''Parse template later
        '''
        self.text = text

    def execute(self, context):
        '''Execute
        '''
        return self.prepare()(context)
