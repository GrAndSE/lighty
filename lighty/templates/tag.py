""" Package provides template tags manager and base tags list """

class TagManager(object):
    """ Class used for tags manipulation """

    def __init__(self):
        """ Create new tag managet instance """
        super(TagManager, self).__init__()
        self.tags = {}

    def register(self, name, tag, is_block_tag=False, context_required=False,
                 template_required=False, loader_required=False):
        """ Register new tag """
        self.tags[name] = (
            tag,
            is_block_tag,
            context_required,
            template_required,
            loader_required
        )

    def is_block_tag(self, name):
        """ Check is block tag """
        if name not in self.tags:
            raise Exception("Tag '%s' is not registered" % name)
        return self.tags[name][1]

    def execute(self, name, token, context, block, template, loader):
        """ Execute tag """
        if name not in self.tags:
            raise Exception("Tag '%s' is not registered" % name)
        tag = self.tags[name]
        args = {
            'token': token
        }
        if tag[1]: args['block']    = block
        if tag[2]: args['context']  = context
        if tag[3]: args['template'] = template
        if tag[4]: args['loader']   = loader
        return tag[0](**args)

tag_manager = TagManager()
