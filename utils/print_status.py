from termcolor import colored

def print_status(status):
    print colored(status, 'green')

def print_error(error):
    print colored(error, 'red')

def print_warning(warning):
    print colored(warning, 'yellow')

def print_success(success):
    print colored(success, 'green', attrs=['bold'])
