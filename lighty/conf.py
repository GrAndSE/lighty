'''Package contains settings management functions
'''

class BaseSettings(object):
    '''Base class for settings mmanagements. Overrides the basics methods
    '''

    def __getattr__(self, name):
        '''Get setting from dictionary
        '''
        if name not in self:
            raise AttributeError("Settings has no attribute '%s'" % name)
        return self.__dict__['config'][name]

    def __dir__(self):
        return self.__dict__['config'].keys()

    def __contains__(self, name):
        return name in self.__dict__['config']

    def load_settings_from_module(self, settings_module):
        '''Load settings from module
        '''
        for setting in dir(settings_module):
            if not setting.startswith('__') and not setting.endswith('__'):
                self.__dict__['config'][setting] = getattr(settings_module,
                                                           setting)
        return self


class ApplicationSettings(BaseSettings):
    '''Class used for local application settings
    '''
    __slots__ = ('config', 'load_settings_from_module', 'postprocess')

    def postprocess(self, global_settings):
        '''You can override this method to make additional operations in child
        class after creation. By default does nothing
        '''
        pass



class Settings(BaseSettings):
    """Class used for settings management 
    """
    __slots__ = ('apps', 'config', 'add_app', 'load_settings', 
                 'load_settings_from_module',)

    def __init__(self):
        '''Create new Settings instance and set default parameters values
        '''
        super(Settings, self).__init__()
        self.__dict__['apps']   = {}
        self.__dict__['config'] = {}

    def load_settings(self, name):
        '''Load settings from specified package
        '''
        settings_module = __import__(name, globals(), locals(), '')
        self.load_settings_from_module(settings_module)
        if 'APPS' in self:
            for app in self.APPS:
                self.add_app(app)
        return self

    def add_app(self, name):
        '''Add application and load it's settings
        '''
        app = __import__(name, globals(), locals(), 'conf')
        if hasattr(app, 'conf'):
            config = getattr(app, 'conf')
            if hasattr(config, '__settings_class__'):
                app_settings = getattr(config, '__settings_class__')()
            else:
                app_settings = ApplicationSettings()
            app_settings.load_settings_from_module(config)
            for setting in dir(app_settings):
                if setting in self:
                    app_settings.__dict__['config'] = getattr(self, setting)
                else:
                    self.__dict__['config'] = getattr(app_settings, setting)
            self.__dict__['apps'][name] = app_settings
            app_settings.postprocess(self)
        return self


settings = Settings()
