'''Tools for run commands in framework environment using simple manage.py 
script
'''
import itertools
import sys
import traceback
import types

from lighty.conf import Settings


def load_commands_from_app(app_name):
    '''Load commands from application with name specified

    Return:
        list of command functions
    '''
    try:
        commands = __import__(app_name + '.commands', globals(), locals(),
                              'commands')
        attrs = [getattr(commands, name) for name in dir(commands)
                 if not name.startswith('_')]
        return [(attr.func_name, attr) for attr in attrs
                if isinstance(attr, types.FunctionType)]
    except ImportError:
        pass
    except:
        traceback.print_exc(file=sys.stdout)
    return []


def load_commands(apps=[]):
    '''Load commands from applications lists
    '''
    commands = [load_commands_from_app(app) for app in apps]
    return dict(itertools.chain(*commands))


def manage():
    '''Process manage command. Load all the commands from applications in
    configuration files and add them into autocompletition
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Lighty manage script',
                                 usage='manage.py --config=conf.cfg command')
    parser.add_argument('--config', default='conf.cfg', type=str,
                        help='configuration file')
    parser.add_argument('command', default='run_server', type=str,
                        help='command to perform')
    args = parser.parse_args()

    try:
        settings = Settings(args.config)
        commands = load_commands(settings.section('APPS'))
    except Exception as e:
        print(e)
    else:
        command = commands[args.commands]
        command(settings)
