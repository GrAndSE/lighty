"""Basic template tags library
"""
import collections
from functools import partial
import itertools
from .template import resolve, Template
from .tag import tag_manager, parse_token


def exec_with_context(func, context={}, context_diff={}):
    old_values = dict([(var_name,
                        context[var_name] if var_name in context else None)
                       for var_name in context_diff])
    context.update(context_diff)
    result = func(context)
    context.update(old_values)
    return result


def exec_block(block, context):
    return "".join([command(context) for command in block])


def block(token, block, template, loader):
    """Block tag
    """
    # Create inner template for blocks
    tmpl = Template(loader)
    tmpl.commands = block

    # Add template block into list
    if not hasattr(template, 'blocks'):
        template.blocks = {}
    is_new = token not in template.blocks
    template.blocks[token] = tmpl

    # Add function that executes inner template into commands
    if is_new:
        return template.blocks[token]
    else:
        index = template.commands.index(template.parent.blocks[token])
        template.commands[index] = tmpl
        return lambda context: ''

tag_manager.register(
        name='block',
        tag=block,
        is_block_tag=True,
        context_required=False,
        template_required=True,
        loader_required=True,
        is_lazy_tag=False
)


def extend(token, template, loader):
    """Tag used to create tamplates hierarhy
    """
    tokens = parse_token(token)[0]
    template.parent = loader.get_template(tokens[0])
    if not hasattr(template, 'blocks'):
        template.blocks = template.parent.blocks.copy()
    else:
        template.blocks.update(template.parent.blocks)
    template.commands.extend(template.parent.commands)
    return None

tag_manager.register(
        name='extend',
        tag=extend,
        template_required=True,
        loader_required=True,
        is_lazy_tag=False
)


def spaceless(token, block, context):
    """This tag removes unused spaces

    Template
        
        {% spaceless %}
            Some
                    text
        {% endspaceless %}

    will be rendered to:
        
        Some text

    """
    results = [command(context).split('\n') for command in block]
    return "".join([line.lstrip() for line in itertools.chain(*results)])

tag_manager.register(
        name='spaceless',
        tag=spaceless,
        is_block_tag=True,
        context_required=True,
        template_required=False,
        loader_required=False,
        is_lazy_tag=True
)


def with_tag(token, block, context):
    """With tag can be used to set the shorter name for variable used few times

    Example:

        {% with request.context.user.name as user_name %}
            <h1>{{ user_name }}'s profile</h1>
            <span>Hello, {{ user_name }}</span>
            <form action="update_profile" method="post">
                <label>Your name:</label>
                <input type="text" name="user_name" value="{{ user_name }}" />
                <input type="submit" value="Update profile" />
            </form>
        {% endwith %}
    """
    data_field, _, var_name = token.split(' ')
    value = resolve(data_field, context)
    return exec_with_context(partial(exec_block, block), 
                               context, {var_name: value})

tag_manager.register(
        name='with',
        tag=with_tag,
        is_block_tag=True,
        context_required=True,
        template_required=False,
        loader_required=False,
        is_lazy_tag=True
)


def if_tag(token, block, context):
    """If tag can brings some logic into template.

    Example:

        {% if user.is_authenticated %}Hello, {{ user.name }}!{% endif %}

    TODO:
        
        - add else
        - add conditions
    """
    if resolve(token, context):
        return exec_block(block, context)
    return ''

tag_manager.register(
        name='if',
        tag=if_tag,
        is_block_tag=True,
        context_required=True,
        template_required=False,
        loader_required=False,
        is_lazy_tag=True
)


class Forloop:
    '''Class for executing block in loop with a context update
    '''

    def __init__(self, var_name, values, block):
        self.var_name = var_name
        self.values = values
        self.block = block

    @property
    def total(self):
        return len(self.values)

    @property
    def last(self):
        return not self.counter0 < self.total
    
    @property
    def first(self):
        return self.counter0 == 0

    @property
    def counter(self):
        return self.counter0 + 1

    def next(self, context):
        self.counter0 = 0
        for v in self.values:
            context[self.var_name] = v
            yield exec_block(self.block, context)

    def __call__(self, context):
        return "".join([next for next in self.next(context)])



def for_tag(token, block, context):
    """For tag

    Example:

        {% for a in items %}{{ a }}{% endfor %}

    returns for items = [1, 2, 3]:
        
        123

    Also forloop variable will be added into scope. It contains few flags can
    be used to render customized templates

        {% for a in items %}
            {% spaceless %}<span
                    {% if forloop.first %} class="first"{% endif %}
                    {% if forloop.last %} class="last"{% endif %}>
                {{ forloop.counter0 }}. 
                {{ forloop.counter }} from {{ forloop.total }}
            </span>{% endspaceless %}
        {% endfor %}

    returns

        <span class="first">0. 1 from 3</span>
        <span>1. 2 from 3</span>
        <span class="last">2. 3 from 3</span>

    """
    var_name, _, data_field = token.split(' ')
    values = resolve(data_field, context)
    # Check values
    if not isinstance(values, collections.Iterable):
        raise ValueError('%s: "%s" is not iterable' % (data_field, values))

    forloop = Forloop(var_name, values, block)
    return exec_with_context(forloop, context, {'forloop': forloop})

tag_manager.register(
        name='for',
        tag=for_tag,
        is_block_tag=True,
        context_required=True,
        template_required=False,
        loader_required=False,
        is_lazy_tag=True
)
