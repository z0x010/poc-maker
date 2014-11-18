#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import os
import sys
import shutil
import argparse

from datetime import date

from utils.env import paths
from utils.env import set_paths
from utils.weekdays import weekdays
from utils.verify_poc import verify_poc
from utils.save_info import save_info
from utils.name_maker import name_maker
from utils.file_maker import file_maker, read_info
from utils.print_status import print_error


def date_maker(words):
    today = str(date.today())
    words['docdate'] = today.replace('-', '/')
    words['pocdate'] = today


def check_weekdays():
    dirname = weekdays()
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def verify_this_poc(poc_filepath, words):
    verify_require = [words['info_target_url'], words['info_test_url'], words['info_match']]
    if all(verify_require):
        verify_path = os.path.join(os.path.abspath('.'), poc_filepath)
        verify_poc(verify_path, verify_require[1])


def verify_this_poc_by_dir(path):
    files = os.listdir(path)
    for _ in files:
        if ('.py' in _) and ('.pyc' not in _):
            poc_filename = _
    verify_path = os.path.join(os.path.abspath(path), poc_filename)
    poc_content = open(verify_path, 'r').read()
    match = re.search('samples = \[(.*?)\]', poc_content)
    if match:
        verify_urls = match.group(1).split(',')
        for _ in verify_urls:
            verify_url = _.strip('\'\" ')
            if verify_url:
                verify_poc(verify_path, verify_url)
    else:
        print_error('[-] can\'t read test_url in {name}'.format(name=poc_filename))


def main():
    set_paths()
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', action='store_true', help='Make week report')
    parser.add_argument('--verify', help='Verify POC by directory eg. 0000_app_1.0_index.php_SQL-Injection')
    parser.add_argument('-i', '--pocinfo', default=paths.INFO_PATH, help='Choice the poc template')
    args = parser.parse_args()
    if args.report:
        make_report()
        sys.exit(0)
    if args.verify:
        verify_this_poc_by_dir(args.verify)
        sys.exit(0)

    poc_info_file = args.pocinfo
    poc_template_file = paths.TEMPLATE_POC_PATH
    doc_template_file = paths.TEMPLATE_DOC_PATH

    words = {}
    read_info(words, poc_info_file)
    date_maker(words)
    poc_name, doc_name = name_maker(words)
    poc_filepath = file_maker(doc_name, poc_name, doc_template_file, poc_template_file, words)
    check_weekdays()
    save_info(poc_info_file, doc_name)
    if poc_filepath:
        verify_this_poc(poc_filepath, words)


if __name__ == "__main__":
    main()
