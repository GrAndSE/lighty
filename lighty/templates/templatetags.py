"""Basic template tags library
"""
from itertools import chain
from template import Template
from tag import tag_manager, parse_token


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


def spaceless(block, context):
    """This tag removes unused spaces

    Template
        
        {% spaceless %}
            Some
                    text
        {% endspaceless %}

    will be rendered to:
        
        Some text

    """
    return "".join([line.lstrip()
                    for line in chain([command(context).split('\n')
                                       for command in block])])


def if_tag(token, block, context):
    """If tag can brings some logic into template.

    Example:

        {% if user.is_authenticated %}Hello, {{ user.name }}!{% endif %}

    TODO:
        
        - add else
        - add conditions
    """
    tokens = parse_token(token)[0]
    fields = tokens[0].split('.')
    if len(fields) > 1:
        fields[0] = context[fields[0]]
        value = reduce(Template.get_field, fields)
    else:
        value = context[tokens[0]]
    if value:
        return "".join([command(context) for command in block])
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
    var_name, _, data_field = parse_token(token)[0]
    fields = data_field.split('.')
    if len(fields) > 1:
        fields[0] = context[fields[0]]
        values = reduce(Template.get_field, fields)
    else:
        values = context[data_field]
    if values:
        new_context = {}
        new_context.update(context)
        length = len(values)
        forloop = {'first': True, 'last': length == 1, 'total': length,
                   'counter0': 0, 'counter': 1}
        new_context['forloop'] = forloop
        results = []
        for v in values:
            new_context[var_name] = v
            forloop['counter'] += 1
            forloop['counter0'] += 1
            forloop['first'] = False
            forloop['last'] = forloop['counter'] < length
            results.append("".join([command(new_context)
                                    for command in block]))
        return "".join(results)
    return ''

tag_manager.register(
        name='for',
        tag=for_tag,
        is_block_tag=True,
        context_required=True,
        template_required=False,
        loader_required=False,
        is_lazy_tag=True
)
