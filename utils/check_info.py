#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import date
from print_status import print_error, print_warning


def check_info(dict):
    info_warning(dict)
    info_error(dict)


def info_warning(dict):
    warning_list = ['appversion', 'vulid', 'appvendor', 'vulreferer', 'vuldesc', 'vuleffect', 'vuldate', 'myname', 'shortname']
    for _ in warning_list:
        if not dict[_]:
            print_warning('[-] Warning: YOU FORGET {0}!'.format(_))
    if dict['vuldate'] == str(date.today()):
        print_warning('[-] Provided Vul published: {0}, the same as today! Are you sure?'.format(dict['vuldate']))


def info_error(dict):
    error_list = ['appname', 'vultype', 'vulpath']
    error = False
    for _ in error_list:
        if not dict[_]:
            print_error('[-] Error: must provide {0}!'.format(_))
            error = True
    if error:
        sys.exit(1)
