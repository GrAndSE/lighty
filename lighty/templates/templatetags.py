""" Basic tags library """
from template import Template
from tag import tag_manager, parse_token


def block(token, block, template, loader):
    """Block tag
    """
    # Create inner template for blocks
    tmpl            = Template(loader)
    tmpl.commands   = block

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
    tokens = parse_token(token)
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
