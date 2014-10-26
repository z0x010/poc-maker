#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import date

def info_warning(dict):
    warning_list = ['appversion', 'vulid', 'appvendor', 'vulreferer', 'vuldesc', 'vuleffect', 'vuldate', 'myname', 'shortname']
    for _ in warning_list:
        if not dict[_]:
            print '[-] Warning: YOU FORGET {0}!'.format(_)
    if dict['vuldate'] == str(date.today()):
        print '[-] Provided Vul published: {0}, the same as today! Are you sure?'.format(dict['vuldate'])


def info_error(dict):
    error_list = ['appname', 'vultype', 'vulpath']
    error = False
    for _ in error_list:
        if not dict[_]:
            print '[-] Error: must provide {0}!'.format(_)
            error = True
    if error:
        sys.exit(1)
