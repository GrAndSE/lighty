'''Package contains settings management functions
'''


class Settings(object):
    """Class used for settings management 
           EMPTY_TUPLES     list of setting by default set as empty tuples
    """

    EMPTY_TUPLES = (
            'MIDDLEWARE_CLASSES',
            'URL_PATTERNS',
            'APPLICATIONS'
    )

    def __init__(self):
        '''Create new Settings instance and set default parameters values
        '''
        super(Settings, self).__init__()
        # Default parameters
        for name in Settings.EMPTY_TUPLES:
            setattr(self, name, ())

    def load_settings(self, name):
        ''' Load settings from specified package '''
        module = __import__(name)
        # Get params
        for name in Settings.EMPTY_TUPLES:
            if hasattr(module, name):
                setattr(self, name, getattr(module, name))


settings = Settings()
