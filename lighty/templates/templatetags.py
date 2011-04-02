""" Basic tags library """

from template import Template
from tag import tag_manager as tag_manager


def block(token, context, block, template, loader):
    """Block tag
    """
    tmpl            = Template(loader)
    tmpl.commands   = block
    print token, context, block, template, loader
    return tmpl.execute(context)

tag_manager.register(
        name='block', 
        tag=block, 
        is_block_tag=True,
        context_required=True,
        template_required=True,
        loader_required=True
)

def extend(token, template, loader):
    """Tag used to create tamplates hierarhy
    """
    print token, template, loader
    #tmpl = loader.get_template()
    #tmpl            = loader
    return ''

tag_manager.register(
        name='extend',
        tag=extend,
        template_required=True,
        loader_required=True
)
