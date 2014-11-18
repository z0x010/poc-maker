#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import sys
import argparse

from utils.env import paths
from utils.env import set_paths
from utils.verify_poc import verify_poc
from utils.save_info import save_info
from utils.name_maker import name_maker
from utils.file_maker import file_maker, read_info


def poc_maker(poc_info, words):
    poc_template_file = paths.TEMPLATE_POC_PATH
    doc_template_file = paths.TEMPLATE_DOC_PATH
    read_info(words, poc_info)
    poc_name, doc_name = name_maker(words)
    poc_filepath = file_maker(doc_name, poc_name, doc_template_file, poc_template_file, words)
    save_info(poc_info, doc_name)
    if poc_filepath:
        verify_poc(poc_filepath, words)


def main():
    words = {}
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
        verify_poc(args.verify, words)
        sys.exit(0)
    poc_info = args.pocinfo

    poc_maker(poc_info, words)


if __name__ == "__main__":
    main()
