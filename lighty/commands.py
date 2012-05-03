'''Tools for run commands in framework environment using simple manage.py
script
'''
import itertools
import sys
import traceback
import types

from lighty.conf import Settings
from lighty.utils import CommandParser, print_func


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


def manage(default_conf='conf.cfg'):
    '''Process manage command. Load all the commands from applications in
    configuration files and add them into autocompletition
    '''
    default_args = ((('arguments', ),
                      {'nargs': 0, 'help': 'command arguments'}), )

    def parse_args(command_arg_type=None, args=default_args):
        parser = CommandParser(description='Lighty manage script')
        parser.add_option('config', 'c', default=default_conf, flag=False,
                          help='configuration file')
        if command_arg_type:
            parser.add_argument('command', type=command_arg_type,
                                optional=False, help='command to execute')
        else:
            parser.add_argument('command', optional=False,
                                help='command to execute')
        for args, kwargs in args:
            parser.add_argument(*args, **kwargs)
        return parser, parser.parse()

    # Get config file
    parser, args = parse_args()
    try:
        settings = Settings(args['config'])
        commands = load_commands(settings.section('APPS'))
    except Exception as e:
        print_func(e)
        print_func(parser.help_text())
        return

    # Try to get command name
    def error_msg(msg):
        raise TypeError('%s. Commands available:\n\t%s\n' % (msg,
                                        "\n\t".join(sorted(commands.keys()))))

    def command_name(name):
        if name == '':
            error_msg('No command specified')
        elif name not in commands:
            error_msg('Wrong command name')
        return name

    parser, args = parse_args(command_name)
    # Parse arguments for code name
    command = commands[args['command']]
    code = command.__code__
    if code.co_argcount > 0:
        call_args = {}
        call_args[code.co_varnames[0]] = settings
        defaults = command.__defaults__ or ()
        arg_index = 1
        defaults_index = 0
        defaults_start = code.co_argcount - len(defaults)
        args = []
        for arg_name in code.co_varnames[1:command.__code__.co_argcount]:
            if defaults_start <= arg_index:
                args.append(((arg_name, ),
                             {'default': defaults[defaults_index]}))
            else:
                args.append(((arg_name, ), {}))
            arg_index += 1
        parser, args = parse_args(command_name, args)
        for arg_name in code.co_varnames[1:command.__code__.co_argcount]:
            call_args[arg_name] = args[arg_name]
        command(**call_args)
    else:
        command()
