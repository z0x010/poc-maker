#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import os
import sys
import shutil
import zipfile
import tempfile
import argparse

from utils import check_info
from utils.weekdays import weekdays
from utils.report_maker import make_report
from utils.print_status import *
from utils.verify_poc import verify_poc
from lxml import etree
from datetime import date
from os.path import splitext, basename


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def get_word_xml():
    doc_template_filename = doc_template_name()
    try:
        zip = zipfile.ZipFile(doc_template_filename)
    except Exception, e:
        print_error('[-] template {name} not exist'.format(name=doc_template_filename))
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
    print_status('[*] reading poc_info')
    for line in open(poc_info_name()):
        if ':=' in line:
            key, word = line.split(':=')
            key = key.strip()
            dict[key] = word.strip().decode('utf-8')
    modify_template(dict)
    print_status('    [*] Name: {0} {1} {2}'.format(dict['appname'], dict['appversion'], dict['vultype']))
    print_status('    [*] Vendor: {0}\n'.format(dict['appvendor']))
    return dict


def modify_template(dict):
    if dict['info_post_data']:
        dict['info_post_data'] = u'payload = \'{data}\'\n        response = req.post(self.url + target_url, data=payload, timeout=10)'.format(data=dict['info_post_data'])
    else:
        dict['info_post_data'] = u'\n        response = req.get(self.url + target_url, timeout=10)'
    if dict['info_match']:
        dict['info_match'] = u'\n        match = re.search(\'{match}\', content)'.format(match=dict['info_match'])
    if dict['info_other_match']:
        dict['info_other_match'] = u'match_other = re.search(\'{match}\', content)\n\n        if match and match_other:'.format(match=dict['info_other_match'])
    else:
        dict['info_other_match'] = u'\n        if match:'


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


def poc_maker(poc_name, words):
    filename = poc_name + '.py'
    poc = open(filename, 'w')
    poc_template_filename = poc_template_name()
    try:
        template = open(poc_template_filename)
    except Exception, e:
        print_error('[-] template {name} not exist'.format(name=poc_template_filename))
    poc_content = template.read().decode('utf-8')
    template.close()
    poc.write(multiple_replace(poc_content, words).encode('utf-8'))
    poc.close()


def file_put_dir(poc_name, doc_name):
    doc_filename = doc_name + '.docx'
    poc_filename = poc_name + '.py'
    poc_filepath = os.path.join(doc_name, poc_filename)
    if not os.path.exists(doc_name):
        os.makedirs(doc_name)
        shutil.move(doc_filename, doc_name)
        shutil.move(poc_filename, doc_name)
        # shutil.copytree(comm_path(), 'comm')
        # shutil.move('comm', doc_name)
    else:
        print_warning('[-] {dir} is exist'.format(dir=doc_name))
        os.remove(poc_filename)
        os.remove(doc_filename)
    print_success('[+] poc_maker have finished')
    return poc_filepath


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
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', action='store_true', help='make week report')
    parser.add_argument('--verify', help='Verify POC by directory eg. 0000_app_1.0_index.php_SQL-Injection')
    args = parser.parse_args()
    if args.report:
        make_report()
        sys.exit(0)
    if args.verify:
        verify_this_poc_by_dir(args.verify)
        sys.exit(0)

    output_path = r''
    words = {}
    read_poc_info(words)
    check_info.info_error(words)
    check_info.info_warning(words)
    date_maker(words)
    xml_from_file = get_word_xml()
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
    poc_filepath = file_put_dir(poc_name, doc_name)
    check_weekdays()
    verify_this_poc(poc_filepath, words)


if __name__ == "__main__":
    main()
