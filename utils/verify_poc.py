#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from pocsuite.utils import get_poc_object

from print_status import *


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


def verify_poc(verify_path, verify_url):
    poc_filename = path.basename(verify_path)
    separator = '=' * 90
    print_status('{separator}\n[*] Verify POC {name} on {url}:'.format(separator=separator, name=poc_filename, url=verify_url))
    poc = get_poc_object(verify_path)
    output = poc.execute(verify_url, default_header, mode='verify', verbose=True)
    output.print_result()
