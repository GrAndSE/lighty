'''Package contains settings management functions
'''
import collections
import itertools
import os
import sys
LIGHTY_CONF_PATH = os.path.realpath(os.path.dirname(__file__))

try:
    # for python 2
    import ConfigParser
    Parser = ConfigParser.SafeConfigParser
except:
    # for python 3
    import configparser
    Parser = configparser.SafeConfigParser


class Settings(collections.Mapping):
    '''Get settings for class
    '''
    __slots__ = ('__init__', '__contains__', '__getattr__', '__getitem__',
                 '__eq__', '__iter__', '__len__', '__ne__', 'configs', 'get',
                 'items', 'keys', 'section', 'sections', 'settings', 'values')

    def __init__(self, main_config, defaults={}):
        '''Load main config, parse it and then trying to load applications from
        all the paths

        Args:
            main_config - main configuration file path
            defaults    - default values
        '''
        # Parse main configurations files, add specified paths and get possible
        # configurations files for an apps
        parser = Parser(defaults, allow_no_value=True)
        parser.read(main_config)
        conf_list = []
        for config_path in parser.options('PATHS'):
            path = os.path.realpath(config_path)
            conf_list.append([os.path.join(path, application, 'conf.cfg')
                              for application in parser.options('APPS')])
            sys.path.append(path)
        conf_list.append([main_config])
        conf_list.append(parser.options('CONFS'))
        # Fill dictionaries
        self.configs = parser.read(itertools.chain(*conf_list))
        self.sections = {}
        self.settings = {}
        for section in parser.sections():
            self.sections[section] = dict([(name, parser.get(section, name))
                                          for name in parser.options(section)])
            self.settings.update(self.sections[section])

    def __getitem__(self, name):
        '''Get value from configuration with specified name

        Arguments:
        '''
        name = name.lower()
        if name in self.settings:
            return self.settings[name]
        for section_name in self.sections:
            if name in self.sections[section_name]:
                return self.sections[section_name][name]
        raise KeyError('"%s" not found in configuration' % name)
    __getattr__ = __getitem__

    def get(self, name, section=None):
        '''Get configuration parameter from sections
        '''
        name = name.lower()
        if section is None:
            if name in self.settings:
                return self.settings[name]
        else:
            if section in self.sections and name in self.sections[section]:     
                return self.sections[section][name]
            else:
                raise KeyError('No section "%s" in configuration' % section)
        raise KeyError('"%s" not found in configuration' % name)

    def section(self, section):
        '''Get all keys from section
        '''
        if section in self.sections:
            return self.sections[section].keys()
        raise KeyError('No section "%s" in configuration' % section)

    def __iter__(self):
        '''Get iterator over the settings keys
        '''
        return self.settings.__iter__()

    def __len__(self):
        '''Get number of unique configuration keys
        '''
        return len(self.settings)

    def keys(self):
        '''Get unique configuration options names
        '''
        return self.settings.keys()

    def values(self):
        '''Get all the configuration options values
        '''
        return self.settings.values()
