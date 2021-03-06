#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import os
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from datetime import date

from utils.print_status import *
from utils.env import module_path


MYNAME = u'flsf'
SHORTNAME = u'flsf'
VULDATE = str(date.today())


info_temp = u"""appname    := {{ appname }}
appversion := {{ appversion }}
appvendor  := {{ appvendor }}

vulid      := {{ vulid }}
vulpath    := {{ vulpath }}
vultype    := {{ vultype }}
vulreferer := {{ vulreferer }}
vuldesc    := {{ vuldesc }}
vuleffect  := {{ vuleffect }}
# 漏洞公布日期
vuldate    := {{ vuldate }}


tools      := {{ tools }}
tooldesc   := {{ tooldesc }}

myname     := {{ myname }}
shortname  := {{ shortname }}


# verify
info_target_url := {{ info_target_url }}
info_post_data  := {{ info_post_data }}
info_match      := {{ info_match }}
info_other_match:= {{ info_other_match }}
info_test_url   := {{ info_test_url }}
"""


SITE = ''
info_words = {'appname': '', 'vuldate': VULDATE, 'vuleffect': '', 'vuldesc': '', 'vultype': '', 'vulid': '',
              'appvendor': '', 'vuldesc': '', 'vulreferer': '', 'tools': '', 'tooldesc': '', 'myname': MYNAME, 'shortname': SHORTNAME, 'info_target_url': '', 'info_post_data': '', 'info_match': '', 'info_other_match': '', 'info_test_url': '', 'appversion': '', 'vulpath': ''}

sql_list = [u'SQL Injection', u'SQL注射']
file_down_list = [u'Arbitrary File Download', u'任意文件遍历/下载']
bypass_list = [u'Login Bypass', u'权限绕过']
upload_list = [u'File Upload', u'上传导致']


def extract_vars(template):
    keys = set()
    for match in re.finditer(r"\{\{ (?P<key>\w+) \}\}", template):
        keys.add(match.groups()[0])
    return sorted(list(keys))


def generate_info(template, context):
    content = template
    for key in extract_vars(template):
        if key not in context:
            raise ValueError("%s is missing from the template context" % key)
        content = content.replace("{{ %s }}" % key, context[key])
    return content


def read_info_content(url):
    print_status('[*] read info from ' + url)
    content = requests.get(url, timeout=5).content
    if SITE == 'wooyun':
        soup = BeautifulSoup(content)
        info_list = soup.find("div", class_="content").find_all("h3")
    elif SITE == 'exp-db':
        info_list = content.split('\n')
    return info_list


def read_vultype(info):
    vultype = u''
    if SITE == 'wooyun':  # 存在修复时间条目,读取不到type,待修复 fixed
        title_info = info[5].string  # 完全公开存在公开时间,读取不到type,待修复,fixed
        if (u'修复时间' in title_info) or (u'公开时间' in title_info):
            title_info = info[6].string

        for sql_key in sql_list:
            if sql_key in title_info:
                vultype = sql_list[0]
                return vultype
        for file_down_key in file_down_list:
            if file_down_key in title_info:
                vultype = file_down_list[0]
                return vultype
        for bypass_key in bypass_list:
            if bypass_key in title_info:
                vultype = bypass_list[0]
                return vultype
        for upload_key in upload_list:
            if upload_key in title_info:
                vultype = upload_list[0]
                return vultype

    elif SITE == 'exp-db':
        if 'multi' in info.lower():
            print_warning('[-] can\'t read multiple vultype')
        for sql_key in sql_list:
            if sql_key in info:
                vultype = sql_list[0]
                return vultype
    return vultype


def read_vulvendor(info):
    if SITE == 'wooyun':
        vendor_info = info[2].a.get("href").encode("utf-8")
        content = requests.get(vendor_info, timeout=5).content
        soup = BeautifulSoup(content)
        try:
            url_info = soup.find("div", class_="content").h3.string
            appvendor = re.search('http.*', url_info).group(0)
        except Exception, e:
            appvendor = ''
    elif SITE == 'exp-db':
        pass
    return appvendor


def read_vuldate(info):
    if SITE == 'wooyun':
        date_info = info[4].string
        vuldate = re.search('20[1-2][3-9]-[0-9]+-[0-9]+', date_info).group(0)
    elif SITE == 'exp-db':
        pass
    return vuldate


def check_site(url):
    global SITE
    if 'wooyun' in url:
        SITE = 'wooyun'
        read_from_wooyun(url)
    elif 'exploit-db' in url:
        SITE = 'exp-db'
        read_from_expdb(url)
    return info_words


def read_from_wooyun(url):
    info = read_info_content(url)
    vultype = read_vultype(info)
    appvendor = read_vulvendor(info)
    vuldate = read_vuldate(info)
    vuleffect = trans_vuleffect(vultype)
    vulreferer = url
    info_words['vultype'] = vultype
    info_words['appvendor'] = appvendor
    info_words['vuldate'] = vuldate
    info_words['vulreferer'] = url
    info_words['vuleffect'] = vuleffect


def read_expdb_title(url):
    title_info = requests.get(url, timeout=5).content
    return title_info.decode('utf-8')


def trans_expdb_info_url(url):
    return url.replace('exploits', 'download')


def read_from_expdb(url):
    title_info = read_expdb_title(url)
    vultype = read_vultype(title_info)
    if vultype:
        info_url = trans_expdb_info_url(url)
        info = read_info_content(info_url)
    info_words['vultype'] = vultype


def clean_info(args):
    if args.appname:
        info_words['appname'] = args.appname
    if args.vulurl:
        info_words['vulreferer'] = args.vulurl
    if args.vultype:
        info_words['vultype'] = trans_vultype(args.vultype)
        if not info_words['vultype']:
            print_warning('[-] can\'t tans {type}'.format(type=args.vultype))
        info_words['vuleffect'] = trans_vuleffect(info_words['vultype'])
    if args.vulid:
        id = args.vulid
        if len(id) == 3:
            id = '0' + id
        info_words['vulid'] = id
    if args.vultool:
        info_words['tools'] = args.vultool
        info_words['tooldesc'] = trans_tools(args.vultool)
    if args.vuldesc:
        info_words['vuldesc'] = args.vuldesc.decode('utf-8')
    if args.target_url:
        info_words['info_target_url'] = args.target_url
    if args.data:
        info_words['info_post_data'] = args.data
    if args.match:
        info_words['info_match'] = args.match
    if args.match_other:
        info_words['info_other_match'] = args.match_other
    if args.test_url:
        info_words['info_test_url'] = args.test_url
    if args.vulpath:
        info_words['vulpath'] = args.vulpath
    if args.appversion:
        info_words['appversion'] = args.appversion

    info_file = os.path.join(module_path(), 'poc_info.txt')
    f = open(info_file, 'w')
    info = generate_info(info_temp, info_words)
    print_status('[*] poc_info {file}\n'.format(file=info_file))
    print info
    f.write(info.encode('utf-8'))
    f.close()
    print_status('[+] poc_clean_info have finished')


def trans_tools(tool):
    key_dic = {
        'sqlmap': u'SQL注入测试工具',
        'firefox': u'浏览器',
        'curl': u'文件传输工具',
    }
    return key_dic.get(tool.lower(), tool)


def trans_vultype(vultype):
    key_dic = {
        'sql': 'SQL Injection',
        'sqli': 'SQL Injection',
        'upload': 'File Upload',
        'fileupload': 'File Upload',
        'rfi': 'Remote File Inclusion',
        'lfi': 'Local File Inclusion',
        'bypass': 'Login Bypass',
        'loginbypass': 'Login Bypass',
        'filedownload': 'Arbitrary File Download',
        'filedown': 'Arbitrary File Download',
        'filedelete': 'Arbitraty File Deletion',
        'filedeletion': 'Arbitraty File Deletion',
        'filede': 'Arbitraty File Deletion',
        'xss': 'Cross Site Scripting',
    }
    return key_dic.get(vultype.lower(), vultype)


def trans_vuleffect(vultype):
    key_dic = {
        'SQL Injection': u'SQL注入,泄露信息',
        'Arbitrary File Download': u'任意文件下载,泄露信息',
        'Arbitrary File Deletion': u'任意文件删除',
        'Login Bypass': u'登录绕过,权限绕过,非授权访问',
        'File Upload': u'文件上传导致代码执行',
    }
    return key_dic.get(vultype, '')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--vulurl', help='Vulnerability Refer url eg. -u http://wooyun.org/bugs/wooyun-2014-073369')
    parser.add_argument('-t', '--vultype', help='Vulnerability Type eg. -t sqli')
    parser.add_argument('-i', '--vulid', help='Vulnerability ID eg. -i 111   id自动补全4位,变为0111')
    parser.add_argument('-o', '--vultool', default='Firefox', help='tools eg.sqlmap or Firefox')
    parser.add_argument('-s', '--vuldesc', help='Vulnerability description')
    parser.add_argument('-n', '--appname', help='APP name eg. wordpress')
    parser.add_argument('-p', '--vulpath', help='Vulnerability path eg. /index.php')

    parser.add_argument('--target-url', dest='target_url', help='Vulnerability target url')
    parser.add_argument('--data', help='Post data')
    parser.add_argument('--test-url', dest='test_url', help='Vulnerability test site')
    parser.add_argument('--appversion', help='APP version eg. 1.0')

    parser.add_argument('-m1', '--match', help='Verify match')
    parser.add_argument('-m2', '--match-other', dest='match_other', help='Verify other match')

    args = parser.parse_args()
    if args.vulurl:
        url = args.vulurl
        check_site(url)

    clean_info(args)

if __name__ == "__main__":
    main()
