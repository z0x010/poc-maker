#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import splitext, basename


def name_maker(words):
    output_path = r''
    doc_name = doc_name_maker(words)
    poc_name = poc_name_maker(words)
    if output_path:
        poc_name = os.path.join(output_path, poc_name)
        doc_name = os.path.join(output_path, doc_name)
    return poc_name, doc_name


def doc_name_maker(words):
    vulname_list = []
    vul_id = words['vulid']
    if not vul_id:
        vul_id = '0000'
    app_name = words['appname'].replace(' ', '-').replace('.', '-')
    vulname_list.append(app_name)
    if words['appversion']:
        app_version = words['appversion'].replace(' ', '-')
        vulname_list.append(app_version)
    vul_path = words['vulpath']
    vul_path = (vul_path[0] == '/' and vul_path[1:].replace('/', '-') or vul_path.replace('/', '-'))
    vulname_list.append(vul_path)
    vul_type = words['vultype'].replace(' ', '-')
    vulname_list.append(vul_type)
    return vul_id + '_' + '_'.join(vulname_list)


def poc_name_maker(words):
    vulname_list = []
    vul_id = words['vulid']
    if not vul_id:
        vul_id = '0000'
    vulname_list.append(vul_id)
    app_name = words['appname'].replace('-', '_').replace('.', '_').replace(' ', '_')
    vulname_list.append(app_name)
    if words['appversion']:
        app_version = words['appversion'].replace('.', '_')
        app_version = app_version.replace(' ', '_')
        vulname_list.append(app_version)
    vul_path = splitext(basename(words['vulpath']))[0]
    vulname_list.append(vul_path)
    vulname_list.append(trans_vultype(words['vultype']).replace(' ', '_'))
    poc_name = '_' + '_'.join(vulname_list)
    return poc_name.lower()


def trans_vultype(vultype):
    vultype = vultype.lower()
    key_dic = {
        'sql': 'sql inj',
        'cross site scripting': 'xss',
        'arbitrary file creation': 'file creation',
        'arbitraty file deletion': 'file deletion',
        'remote password': 'remote pass change',
        'backup file found': 'bak file found',
        'command': 'cmd exec',
        'arbitraty file download': 'file download',
        'information disclosure': 'info disclosure',
        'code': 'code exec',
        'traversal': 'dir traversal',
        'remote file': 'rfi',
        'local file': 'lfi'
    }
    for _ in key_dic:
        if _ in vultype:
            return key_dic[_]
    return vultype
