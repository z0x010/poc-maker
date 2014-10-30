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


def get_template_file(template):
    if template == 'pocsuite':
        doc_template = os.path.join(cur_file_dir(), 'template/poc_template.docx')
        poc_template = os.path.join(cur_file_dir(), 'template/new_poc_template.txt')
    else:
        doc_template = os.path.join(cur_file_dir(), 'template/poc_template.docx')
        poc_template = os.path.join(cur_file_dir(), 'template/poc_template.txt')
    return poc_template, doc_template


def comm_path():
    return os.path.join(cur_file_dir(), 'template/comm')

