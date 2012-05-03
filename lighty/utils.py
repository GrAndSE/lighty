'''Some utilitary classes usually used to make working with different python
versions and different environment easier:

- string_types - basestring for python 2 and str fot python 3
- dict_keys - convert dict keys to list
- div_operators - operators for division
- with_metaclass - metaclasses
'''
import getopt
import operator
import sys


def print_func(*args):
    sys.stdout.write(' '.join([str(arg) for arg in args]))
    sys.stdout.write('\n')

PY3 = sys.version_info[0] == 3
div_operators = (operator.__truediv__, operator.__floordiv__)
if PY3:
    string_types = str
    dict_keys = lambda keys: [i for i in keys.__iter__()]
else:
    string_types = basestring
    dict_keys = lambda keys: keys
    div_operators += (operator.__div__, )


def with_metaclass(meta, base=object):
    '''Create a new class with base class base and metaclass metaclass. This is
    designed to be used in class declarations like this::

        from lighty.utils import with_metaclass

        class Meta(type):
            pass

        class Base(object):
            pass

        class MyClass(with_metaclass(Meta, Base)):
            pass
    '''
    return meta("NewBase", (base, ), {})


class Argument(object):
    '''Command line argument class
    '''

    def __init__(self, name, flag=True, optional=True, default=None, help='',
                 type=str, nargs=1):
        self.name = name
        self.flag = flag
        self.optional = optional or flag
        self.default = default
        self.help = help
        self.type = type
        self.nargs = nargs


class CommandParser(object):
    '''Class for parsing command line arguments
    '''

    def __init__(self, program=None, description='', help=''):
        self.options = {}
        self.arguments = []
        self.program = program if program else sys.argv[0]
        self.description = description
        self.help = help

    def add_option(self, name, *args, **kwargs):
        '''Add an option
        '''
        argument = Argument(name, **kwargs)
        self.options[name] = argument
        for alias in args:
            self.options[alias] = argument

    def add_argument(self, name, **kwargs):
        '''Add an argument
        '''
        kwargs['flag'] = False
        self.arguments.append(Argument(name, **kwargs))

    def help_text(self):
        '''Get usage string
        '''
        args = []
        args_help = []
        for alias in self.options:
            option = self.options[alias]
            if option.name == alias:
                args_help.append(alias + ':\t' + option.help)
                name = '--' + alias if len(alias) > 1 else '-' + alias
                if option.flag:
                    arg = name
                elif option.default:
                    arg = name + '=' + option.default
                else:
                    arg = name + '=value'
                args.append('[%s]' % arg if option.optional else arg)
        for argument in self.arguments:
            if argument.nargs > 1:
                name = ' '.join(['%s%s' % (argument.name, i)
                                for i in range(argument.nargs)])
            elif argument.nargs < 1:
                name = argument.name + ' ...'
            else:
                name = argument.name
            args.append(('[%s]' % name) if argument.optional else name)
            args_help.append(argument.name + ':\t' + argument.help)
        return '%s\n\nUsage:\n\t%s %s\n\nArguments:\n\t%s\n' % (
                self.description, self.program, ' '.join(args),
                '\n\t'.join(args_help))

    def parse(self, args=None):
        '''Parse arguments specified and if there is no arguments specified
        parse a command line arguments
        '''
        try:
            if args is None:
                args = sys.argv[1:]
            result = {}
            result = self._parse(args)
        except (TypeError, LookupError) as ex:
            print_func('%s:' % self.program, ex, '\n')
            print_func(self.help_text())
            sys.exit(-1)
        else:
            return result

    def _parse(self, args_for_parse):
        '''Parse arguments specified and raise an exception when something goes
        wrong
        '''
        options = [(opt if self.options[opt].flag else opt + '=')
                   for opt in self.options if len(opt) > 1]
        soptions = ''.join([(opt if self.options[opt].flag else opt + ':')
                            for opt in self.options if len(opt) == 1])
        opts, args = getopt.getopt(args_for_parse, soptions, options)
        result = {}
        # Get option values
        for key, value in opts:
            alias = key[2:] if key.startswith('--') else key[1:]
            option = self.options[alias]
            if value or value == '':
                if value.startswith('='):
                    value = value[1:]
                result[option.name] = option.type(value)
            elif (option.optional or option.flag) and option.default:
                result[option.name] = option.type(option.default)
        # Get default values
        for alias in self.options:
            option = self.options[alias]
            if option.name not in result:
                if option.default:
                    result[option.name] = option.default
                elif not option.optional:
                    raise LookupError(option.name + ' value missed')
        # Arguments
        index = 0
        for argument in self.arguments:
            if index >= len(args):
                # Check for default value if there is no value specified
                if argument.optional:
                    if argument.default:
                        result[argument.name] = argument.default
                else:
                    raise LookupError(argument.name + ' value missed')
            else:
                if argument.nargs > 1:
                    ni = index + argument.nargs
                    result[argument.name] = [argument.type(value)
                                             for value in args[index:ni]]
                    index = ni
                elif argument.nargs == 1:
                    result[argument.name] = argument.type(args[index])
                    index += 1
                else:
                    result[argument.name] = [argument.type(value)
                                             for value in args[index:]]
                    index = len(args)
        return result
