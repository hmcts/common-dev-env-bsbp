import argparse
from argparse import RawTextHelpFormatter

def get_parser():
    parser = argparse.ArgumentParser(description='Run arguments for dev-env', formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', nargs='*', default=[], help='%s%s%s' % ( \
        '1) start service all (start all services) \n', 
        '2) start service <service> (start specific service - i.e bulk-scan-orchestrator) \n',
        '3) <no args> (default, prompt to start all services)'))
    return parser