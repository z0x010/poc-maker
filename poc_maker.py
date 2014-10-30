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

from utils import env
from utils.print_status import *
from utils.weekdays import weekdays
from utils.check_info import check_info
from utils.verify_poc import verify_poc
from utils.save_info import save_info
from utils.modify_template import modify_poc_template
from utils.name_maker import name_maker
from lxml import etree
from datetime import date


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def get_word_xml(doc_template_file):
    try:
        zip = zipfile.ZipFile(doc_template_file)
    except Exception, e:
        print_error('[-] template {name} does not exist'.format(name=doc_template_file))
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


def write_and_close_docx(xml_content, doc_name, doc_template_file):
    tmp_dir = tempfile.mkdtemp()
    zip = zipfile.ZipFile(doc_template_file)
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


def read_poc_info(dict, poc_info_file):
    print_status('[*] reading poc_info')
    for line in open(poc_info_file):
        if ':=' in line:
            key, word = line.split(':=')
            key = key.strip()
            dict[key] = word.strip().decode('utf-8')
    modify_poc_template(dict)
    print_status('    [*] Name: {0} {1} {2}'.format(dict['appname'], dict['appversion'], dict['vultype']))
    print_status('    [*] Vendor: {0}'.format(dict['appvendor']))
    return dict


def poc_maker(poc_name, words, poc_template_file):
    filename = poc_name + '.py'
    poc = open(filename, 'w')
    try:
        template = open(poc_template_file)
    except Exception, e:
        print_error('[-] template {name} does not exist'.format(name=poc_template_file))
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
        # shutil.copytree(env.comm_path(), 'comm')
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


def doc_maker(doc_name, words, doc_template_file):
    xml_from_file = get_word_xml(doc_template_file)
    xml_tree = get_xml_tree(xml_from_file)
    for node, text in itertext(xml_tree, words):
        pass
    write_and_close_docx(xml_tree, doc_name, doc_template_file)


def read_info(words, poc_info_file):
    read_poc_info(words, poc_info_file)
    check_info(words)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', action='store_true', help='Make week report')
    parser.add_argument('--verify', help='Verify POC by directory eg. 0000_app_1.0_index.php_SQL-Injection')
    parser.add_argument('-t', '--template', default='pocsuite', help='Choice the poc template')
    parser.add_argument('-i', '--pocinfo', default=env.poc_info_name(), help='Choice the poc template')
    args = parser.parse_args()
    if args.report:
        make_report()
        sys.exit(0)
    if args.verify:
        verify_this_poc_by_dir(args.verify)
        sys.exit(0)

    poc_info_file = args.pocinfo
    poc_template_file, doc_template_file = env.get_template_file(args.template)

    words = {}
    read_info(words, poc_info_file)
    date_maker(words)
    poc_name, doc_name = name_maker(words)

    doc_maker(doc_name, words, doc_template_file)
    poc_maker(poc_name, words, poc_template_file)

    poc_filepath = file_put_dir(poc_name, doc_name)
    check_weekdays()
    save_info(poc_info_file, doc_name)
    verify_this_poc(poc_filepath, words)


if __name__ == "__main__":
    main()
