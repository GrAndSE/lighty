""" Basic tags library """

from template import Template
from tag import tag_manager as tag_manager


def block(token, context, block, template, loader):
    tmpl            = Template(loader)
    tmpl.commands   = block
    return tmpl.execute(context)
tag_manager.register(
        name='block', 
        tag=block, 
        is_block_tag=True,
        context_required=True,
        template_required=True,
        loader_required=True
)
