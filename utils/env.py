#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def poc_info_name():
    return os.path.join(cur_file_dir(), 'poc_info.txt')


def doc_template_name():
    return os.path.join(cur_file_dir(), 'template/poc_template.docx')


def poc_template_name():
    return os.path.join(cur_file_dir(), 'template/new_poc_template.txt')


def comm_path():
    return os.path.join(cur_file_dir(), 'template/comm')

