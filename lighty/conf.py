'''Package contains settings management functions
'''
import collections
import itertools
import os
import sys
from .utils import dict_keys
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
                 '__eq__', '__iter__', '__len__', '__ne__', '_sections',
                 '_settings', 'get', 'items', 'keys', 'section', 'sections',
                 'values', )

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
        if len(parser.read(main_config)) == 0:
            raise LookupError('Could not load configuration: %s' % main_config)
        conf_list = []
        for config_path in parser.options('PATHS'):
            path = os.path.realpath(config_path)
            conf_list.append([os.path.join(path, application, 'conf.cfg')
                              for application in parser.options('APPS')])
            sys.path.append(path)
        conf_list.append([main_config])
        conf_list.append(parser.options('CONFS'))
        # Fill dictionaries
        parser.read(itertools.chain(*conf_list))
        self._sections = {}
        self._settings = {}
        for section in parser.sections():
            self._sections[section] = dict([(name, parser.get(section, name))
                                        for name in parser.options(section)])
            self._settings.update(self._sections[section])

    def __getitem__(self, name):
        '''Get value from configuration with specified name

        Args:
            name - option name

        Returns:
            last defined value for an option with specified from all the
            configuration files and their sections

        Raises:
            KeyError - if there is no option with specified name found in all
            configuration files
        '''
        name = name.lower()
        if name in self._settings:
            return self._settings[name]
        for section_name in self._sections:
            if name in self._sections[section_name]:
                return self._sections[section_name][name]
        raise KeyError('"%s" not found in configuration' % name)
    __getattr__ = __getitem__

    def get(self, name, section=None):
        '''Get configuration parameter from sections

        Args:
            name: item name
            section: section name

        Returns:
            value stored in configuration wit specified name
        '''
        name = name.lower()
        if section is None:
            if name in self._settings:
                return self._settings[name]
        else:
            if section in self._sections and name in self._sections[section]:
                return self._sections[section][name]
            else:
                raise KeyError('No section "%s" in configuration' % section)
        raise KeyError('"%s" not found in configuration' % name)

    def section_options(self, section):
        '''Get all keys from section

        Args:
            section - section name

        Returns:
            dictionary contains all the settings names from section
        '''
        if section in self._sections:
            return dict_keys(self._sections[section].keys())
        raise KeyError('No section "%s" in configuration' % section)

    def section(self, section):
        '''Get the dictionary of keys and values from section

        Args:
            section - section name

        Returns:
            dictionary contains all the settings from sections
        '''
        if section in self._sections:
            return self._sections[section].copy()
        raise KeyError('No section "%s" in configuration' % section)

    def has_section(self, section):
        '''Check is section in configuration exists

        Args:
            section - section name

        Returns:
            True if section exists or False if not
        '''
        return section in self._sections

    def sections(self):
        '''Get a section names list
        '''
        return self._sections.keys()

    def __iter__(self):
        '''Get iterator over the settings keys
        '''
        return self._settings.__iter__()

    def __len__(self):
        '''Get number of unique configuration keys
        '''
        return len(self._settings)

    def keys(self):
        '''Get unique configuration options names
        '''
        return self._settings.keys()

    def values(self):
        '''Get all the configuration options values
        '''
        return self._settings.values()
