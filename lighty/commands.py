'''Tools for run commands in framework environment using simple manage.py 
script
'''
from lighty.conf import Settings
from lighty.wsgi import commands

def manage():
    '''Manage script
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
    except Exception as e:
        print(e)
    else:
        command = getattr(commands, args.command)
        command(settings)
