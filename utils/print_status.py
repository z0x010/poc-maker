import sys
from termcolor import colored

def print_status(status):
    print colored(status, 'green')

def print_error(error):
    print colored(error, 'red')
    sys.exit(0)

def print_warning(warning):
    print colored(warning, 'yellow')

def print_success(success):
    print colored(success, 'green', attrs=['bold'])
