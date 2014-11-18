#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from print_status import *

try:
    from pocsuite.utils import get_poc_object
except Exception, e:
    pass

default_header = {
    'Accept': '*/*',
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com',
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; '
                   'WOW64) AppleWebKit/537.17 (KHTML, like Gecko) '
                   'Chrome/24.0.1312.52 Safari/537.17')
}


def verify_poc(path, words):
    if not words:
        verify_this_poc_by_dir(path)
    else:
        verify_this_poc(path, words)


def verify_this_poc(poc_filepath, words):
    verify_require = [words['info_target_url'], words['info_test_url'], words['info_match']]
    if all(verify_require):
        verify_path = os.path.join(os.path.abspath('.'), poc_filepath)
        verify(verify_path, verify_require[1])


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
                verify(verify_path, verify_url)
    else:
        print_error('[-] can\'t read test_url in {name}'.format(name=poc_filename))


def verify(verify_path, verify_url):
    poc_filename = os.path.basename(verify_path)
    separator = '=' * 40
    print separator
    print_status('[*] Verify POC {name} on {url}:'.format(name=poc_filename, url=verify_url))
    try:
        poc = get_poc_object(verify_path)
    except Exception, e:
        print_error('[-] No module named pocsuite.utils can\'t verify this poc, please manual verify')

    result = poc.execute(verify_url, default_header, mode='verify', verbose=True)
    if result.status == 1:
        for k, v in result.result.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    print '    [*] %s : %s' % (kk, vv)
        else:
            print '    [*] %s : %s' % (k, v)
        print_success('[+] Verify POC have finished')
    else:
        print_error('[-] Verify POC failed, please manual verify')
