'''Package contains settings management functions
'''


class Settings(object):
    """Class used for settings management 
    """
    __slots__ = ('apps', 'config', 'add_app', 'load_settings', )

    def __init__(self):
        '''Create new Settings instance and set default parameters values
        '''
        super(Settings, self).__init__()
        self.apps   = []
        self.config = {}

    def load_settings(self, name):
        '''Load settings from specified package
        '''
        app = __import__(name, globals(), locals(), 'conf')
        if hasattr(app, 'conf'):
            config = getattr(app, 'conf')
            for setting in config:
                self.config[setting] = getattr(config, setting)
        return self

    def add_app(self, name):
        '''Add application and load it's settings
        '''
        self.load_settings(name)
        self.apps.append(name)
        return self

settings = Settings()
