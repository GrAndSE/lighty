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
        return [(attr.__name__, attr) for attr in attrs
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
    # Get config file
    parser = argparse.ArgumentParser(description='Lighty manage script')
    parser.add_argument('--config', '-c', default='conf.cfg',
                        help='configuration file')
    parser.add_argument('command', default='', help='command to execute')
    parser.add_argument('arguments', nargs='*', help='command arguments')
    args = parser.parse_args()
    try:
        settings = Settings(args.config)
        commands = load_commands(settings.section('APPS'))
    except Exception as e:
        print(e)
        return

    # Try to get command name
    def error_msg(msg):
        raise argparse.ArgumentTypeError('%s. Commands available:\n\t%s\n' % (
                                    msg, "\n\t".join(sorted(commands.keys()))))

    def command_name(name):
        if name == '':
            error_msg('No command specified')
        elif name not in commands:
            error_msg('No command specified')
        return name

    parser = argparse.ArgumentParser(description='Lighty manage script',
                    usage='manage.py [-h] --config %s command' % args.config)
    parser.add_argument('--config', '-c', default='conf.cfg',
                        help='configuration file')
    parser.add_argument('command', type=command_name,
                        help='command to execute')
    parser.add_argument('arguments', nargs='*', help='command arguments')
    args = parser.parse_args()
    # Parse arguments for code name
    parser = argparse.ArgumentParser(description='Lighty manage script')
    parser.add_argument('--config', '-c', default='conf.cfg',
                        help='configuration file')
    parser.add_argument('command', type=command_name,
                        help='command to execute')
    command = commands[args.command]
    code = command.__code__
    if code.co_argcount > 0:
        call_args = {}
        call_args[code.co_varnames[0]] = settings
        defaults = command.__defaults__ or ()
        arg_index = 1
        defaults_index = 0
        defaults_start = code.co_argcount - len(defaults)
        for arg_name in code.co_varnames[1:command.__code__.co_argcount]:
            if defaults_start <= arg_index:
                parser.add_argument(arg_name, default=defaults[defaults_index])
            else:
                parser.add_argument(arg_name)
            arg_index += 1
        args = parser.parse_args()
        for arg_name in code.co_varnames[1:command.__code__.co_argcount]:
            call_args[arg_name] = getattr(args, arg_name)
        command(**call_args)
    else:
        command()
