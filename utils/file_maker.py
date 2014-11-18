#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import zipfile
import tempfile

from lxml import etree
from env import paths
from print_status import *
from check_info import check_info
from modify_template import modify_poc_template


def file_maker(doc_name, poc_name, doc_template_file, poc_template_file, words):
    doc_maker(doc_name, words, doc_template_file)
    poc_maker(poc_name, words, poc_template_file)
    poc_filepath = file_put_dir(poc_name, doc_name)
    return poc_filepath


def doc_maker(doc_name, words, doc_template_file):
    xml_from_file = get_word_xml(doc_template_file)
    xml_tree = get_xml_tree(xml_from_file)
    for node, text in itertext(xml_tree, words):
        pass
    write_and_close_docx(xml_tree, doc_name, doc_template_file)


def poc_maker(poc_name, words, poc_template_file):
    filename = poc_name + '.py'
    filepath = os.path.join(paths.ROOT_PATH, filename)
    poc = open(filepath, 'w')
    try:
        template = open(poc_template_file)
    except Exception, e:
        print_error('[-] poc template {name} does not exist'.format(name=poc_template_file))
    poc_content = template.read().decode('utf-8')
    template.close()
    poc.write(multiple_replace(poc_content, words).encode('utf-8'))
    poc.close()


def file_put_dir(poc_name, doc_name):
    doc_filename = doc_name + '.docx'
    poc_filename = poc_name + '.py'
    ROOT_PATH = paths.ROOT_PATH
    doc_filepath = os.path.join(ROOT_PATH, doc_filename)
    poc_filepath = os.path.join(ROOT_PATH, poc_filename)
    poc_dirpath = os.path.join(ROOT_PATH, doc_name)
    if not os.path.exists(poc_dirpath):
        os.makedirs(poc_dirpath)
        shutil.move(doc_filepath, poc_dirpath)
        shutil.move(poc_filepath, poc_dirpath)
        # shutil.copytree(paths.COMM_PATH, 'comm')
        # shutil.move('comm', poa_dirname)
    else:
        print_warning('[-] {dir} is exist'.format(dir=poc_dirpath))
        os.remove(poc_filepath)
        os.remove(doc_filepath)
    print_success('[+] poc_maker have finished')
    return os.path.join(poc_dirpath, poc_name)


def get_word_xml(doc_template_file):
    try:
        zip = zipfile.ZipFile(doc_template_file)
    except Exception, e:
        print_error('[-] doc template {name} does not exist'.format(name=doc_template_file))
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
    output_filepath = os.path.join(paths.ROOT_PATH, output_filename)
    zip_copy_filename = output_filepath
    with zipfile.ZipFile(zip_copy_filename, "w") as docx:
        for filename in filenames:
            docx.write(os.path.join(tmp_dir, filename), filename)
    shutil.rmtree(tmp_dir)


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def read_info(words, poc_info_file):
    read_poc_info(words, poc_info_file)
    check_info(words)


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
