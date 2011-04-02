"""Package provides template tags manager and base tags list 
"""

def parse_token(token):
    tokens = []
    delim = None
    sentence = None
    for word in [word for word in token.split(' ') if len(word) > 0]:
        if delim is None:
            idx = word.find('"')
            if idx < 0:
                idx = word.find("'")
            if idx >= 0:
                delim = word[idx]
                if idx > 0:
                    tokens.append(word[0:idx])
                word = word[idx+1:]
                if delim in word:
                    parts = word.split(delim)
                    tokens.append(parts[0])
                    if len(parts) > 1 and len(parts[1]) > 0:
                        tokens.append(parts[1])
                    delim = None
                else:
                    sentence = [word]
            else: 
                tokens.append(word)
        else:
            if delim in word:
                parts = word.split(delim)
                sentence.append(parts[0])
                tokens.append(" ".join(sentence))
                if len(parts) > 1 and len(parts[1]) > 0:
                    tokens.append(parts[1])
                delim = None
            else:
                sentence.append(word)
    return tokens
                

class TagManager(object):
    """Class used for tags manipulation 
    """

    def __init__(self):
        """Create new tag managet instance 
        """
        super(TagManager, self).__init__()
        self.tags = {}

    def register(self, name, tag, is_block_tag=False, context_required=False,
                 template_required=False, loader_required=False):
        """Register new tag
        """
        self.tags[name] = (
            tag,
            is_block_tag,
            context_required,
            template_required,
            loader_required
        )

    def is_tag_exists(self, name):
        """Check is tag exists
        """
        if name not in self.tags:
            raise Exception("Tag '%s' is not registered" % name)

    def execute(self, name, token, context, block, template, loader):
        """Execute tag 
        """
        self.is_tag_exists(name)
        tag = self.tags[name]
        args = {
            'token': token
        }
        if tag[1]: args['block'] = block
        if tag[2]: args['context'] = context
        if tag[3]: args['template'] = template
        if tag[4]: args['loader'] = loader
        return tag[0](**args)

    def is_block_tag(self, name):
        """Check is tag with specified name is block tag
        """
        self.is_tag_exists(name)
        return self.tags[name][1]


tag_manager = TagManager()
