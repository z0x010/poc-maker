#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import os
import sys
import shutil
import zipfile
import tempfile

from lxml import etree
from datetime import date
from os.path import splitext, basename

from utils.weekdays import weekdays


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def get_word_xml(doc_template_filename):
    zip = zipfile.ZipFile(doc_template_filename)
    xml_content = zip.read('word/document.xml')
    return xml_content


def get_xml_tree(xml_string):
    return etree.fromstring(xml_string)


def itertext(my_etree, words):
    for node in my_etree.iter(tag=etree.Element):
        if check_element_is(node, 't'):
            if node.text in words:
                node.text = words[node.text]
            yield (node, node.text)


def check_element_is(element, type_char):
    word_schema = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    return element.tag == '{%s}%s' % (word_schema, type_char)


def write_and_close_docx(xml_content, doc_name):
    tmp_dir = tempfile.mkdtemp()
    zip = zipfile.ZipFile(doc_template_name())
    zip.extractall(tmp_dir)
    with open(os.path.join(tmp_dir, 'word/document.xml'), 'w') as f:
        xmlstr = etree.tostring(xml_content, pretty_print=True)
        f.write(xmlstr)
    filenames = zip.namelist()
    output_filename = doc_name + '.docx'
    zip_copy_filename = output_filename
    with zipfile.ZipFile(zip_copy_filename, "w") as docx:
        for filename in filenames:
            docx.write(os.path.join(tmp_dir, filename), filename)
    shutil.rmtree(tmp_dir)


def read_poc_info(dict):
    print '[*] reading poc_info'
    for line in open(poc_info_name()):
        if ':=' in line:
            key, word = line.split(':=')
            key = key.strip()
            dict[key] = word.strip().decode('utf-8')
    print '[*] Name: {0} {1} {2}'.format(dict['appname'], dict['appversion'], dict['vultype'])
    print '[*] Vendor: {0}'.format(dict['appvendor'])
    return dict


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


def doc_name_maker(words):
    vulname_list = []
    vul_id = words['vulid']
    app_name = words['appname'].replace(' ', '-')
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
    vulname_list.append(words['vulid'])
    app_name = words['appname']
    if '-' in app_name:
        app_name = app_name.replace('-', '_')
    if ' ' in app_name:
        app_name = app_name.replace(' ', '_')
    vulname_list.append(app_name)
    if words['appversion']:
        app_version = words['appversion'].replace('.', '_')
        app_version = app_version.replace(' ', '_')
        vulname_list.append(app_version)
    vul_path = splitext(basename(words['vulpath']))[0]
    vulname_list.append(vul_path)
    vulname_list.append(trans_vultype(words['vultype']).replace(' ', '_'))
    poc_name =  '_' + '_'.join(vulname_list)
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


def poc_maker(poc_name, words):
    filename = poc_name + '.py'
    poc = open(filename, 'w')
    template = open(poc_template_name())
    poc_content = template.read().decode('utf-8')
    template.close()
    poc.write(multiple_replace(poc_content, words).encode('utf-8'))
    poc.close()


def file_put_dir(poc_name, doc_name):
    if not os.path.exists(doc_name):
        os.makedirs(doc_name)
    doc_filename = doc_name + '.docx'
    poc_filename = poc_name + '.py'
    print '[*] makeing ' + doc_filename
    print '[*] makeing ' + poc_filename
    shutil.move(doc_filename, doc_name)
    shutil.move(poc_filename, doc_name)
    # shutil.copytree(comm_path(), 'comm')
    # shutil.move('comm', doc_name)
    print '[+] poc_maker have finished'


def date_maker(words):
    today = str(date.today())
    words['docdate'] = today.replace('-', '/')
    words['pocdate'] = today


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def poc_info_name():
    try:
        return sys.argv[1]
    except:
        return os.path.join(cur_file_dir(), 'poc_info.txt')


def doc_template_name():
    return os.path.join(cur_file_dir(), 'template/poc_template.docx')


def poc_template_name():
    return os.path.join(cur_file_dir(), 'template/new_poc_template.txt')

def comm_path():
    return os.path.join(cur_file_dir(), 'template/comm')

def check_weekdays():
    dirname = weekdays()
    if not os.path.exists(dirname):
        os.makedirs(dirname)



if __name__ == "__main__":
    output_path = r''
    words = {}
    read_poc_info(words)
    info_error(words)
    info_warning(words)
    date_maker(words)
    xml_from_file = get_word_xml(doc_template_name())
    xml_tree = get_xml_tree(xml_from_file)
    for node, text in itertext(xml_tree, words):
        pass
    doc_name = doc_name_maker(words)
    poc_name = poc_name_maker(words)
    if output_path:
        poc_name = os.path.join(output_path, poc_name)
        doc_name = os.path.join(output_path, doc_name)
    write_and_close_docx(xml_tree, doc_name)
    poc_maker(poc_name, words)
    file_put_dir(poc_name, doc_name)
    check_weekdays()
