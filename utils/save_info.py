#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from print_status import *
from env import paths


def save_info(info_file, poc_name):
    print '=' * 40
    print_status('[*] save poc_info:')
    info_dir = os.path.join(paths.ROOT_PATH, 'info_bak')
    saved_file = os.path.join(info_dir, poc_name) + '.txt'
    if not os.path.exists(info_dir):
        os.makedirs(info_dir)
    if os.path.exists(saved_file):
        print_warning('    [-] {name} exist, it will be replaced'.format(name=poc_name))
    else:
        print_status('    [*] {name} will be saved'.format(name=poc_name))

    try:
        shutil.copyfile(info_file, saved_file)
    except Exception, e:
        print_warning('    [-] save_info failed')
    else:
        print_success('[+] save_info have finished')
