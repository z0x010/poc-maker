#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import sys
import requests
from bs4 import BeautifulSoup

info_temp = u"""appname    := 
appversion := 
appvendor  := {{ vulvendor }}

vulid      := 
vulpath    := 
vultype    := {{ vultype }}
vulreferer := {{ vulreferer }}
vuldesc    :=
vuleffect  := {{ vuleffect }}
# 漏洞公布日期
vuldate    := {{ vuldate }}


tools      := {{ tools }}
tooldesc   := {{ toolsdesc }}

myname     := {{ myname }}
shortname  := {{ shortname }}
"""

MYNAME = u''
SHORTNAME = u''
TOOLS = u'Firefox'
TOOLSDESC = u'浏览器'
VULDATE = u'2014-09-'

SITE = ''

info_words = {'vuldate': VULDATE, 'vuleffect': '', 'vultype': '', 'vulvendor': '', 'vuldesc': '', 'vulreferer': '', 'tools': TOOLS, 'toolsdesc': TOOLSDESC, 'myname': MYNAME, 'shortname': SHORTNAME}

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
    print '[*] read info from ' + url
    content = requests.get(url).content
    if SITE == 'wooyun':
        soup = BeautifulSoup(content)
        info_list = soup.find("div", class_="content").find_all("h3")
    elif SITE == 'exp-db':
        info_list = content.split('\n')
    return info_list

def read_vultype(info):
    vultype = u''
    if SITE == 'wooyun': # 存在修复时间条目,读取不到type,带修复 fixed
        title_info = info[5].string
        if u'修复时间' in title_info:
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
            print '[-] can\'t read multiple vultype'
            sys.exit(0)
        for sql_key in sql_list:
            if sql_key in info:
                vultype = sql_list[0]
                return vultype
    return vultype

def read_vulvendor(info):
    if SITE == 'wooyun':
        vendor_info = info[2].a.get("href").encode("utf-8")
        content = requests.get(vendor_info).content
        soup = BeautifulSoup(content)
        try:
            url_info = soup.find("div", class_="content").h3.string
            vulvendor = re.search('http.*', url_info).group(0)
        except Exception, e:
            vulvendor = ''
    elif SITE == 'exp-db':
        pass
    return vulvendor

def read_vuldate(info):
    if SITE == 'wooyun':
        date_info = info[4].string
        vuldate = re.search('20[1-2][3-9]-[0-9]+-[0-9]+', date_info).group(0)
    elif SITE == 'exp-db':
        pass
    return vuldate

def read_vuleffect(vultype):
    vuleffect = ''
    if vultype == 'SQL Injection':
        vuleffect = u'SQL注入,泄露信息'
    elif vultype == 'Arbitrary File Download':
        vuleffect = u'任意文件下载,泄露信息'
    elif vultype == 'Login Bypass':
        vuleffect = u'登录绕过,权限绕过,非授权访问'
    elif vultype == 'File Upload':
        vuleffect = u'文件上传导致代码执行'
    return vuleffect

def check_site(url):
    global SITE
    if 'wooyun' in url:
        SITE = 'wooyun'
        read_from_wooyun(url)
    elif 'exploit-db' in url:
        SITE = 'exp-db'
        read_from_expdb(url)

def read_from_wooyun(url):
    info = read_info_content(url)
    vultype = read_vultype(info)
    vulvendor = read_vulvendor(info)
    vuldate = read_vuldate(info)
    vuleffect = read_vuleffect(vultype)
    vulreferer = url
    info_words['vultype'] = vultype
    info_words['vulvendor'] = vulvendor
    info_words['vuldate'] = vuldate
    info_words['vulreferer'] = url
    info_words['vuleffect'] = vuleffect

def read_expdb_title(url):
    title_info = requests.get(url).content
    return title_info

def trans_expdb_info_url(url):
    return url.replace('exploits', 'download')

def read_from_expdb(url):
    title_info = read_expdb_title(url)
    vultype = read_vultype(title_info)
    info_url = trans_expdb_info_url(url)
    info = read_info_content(info_url)

    info_words['vultype'] = vultype

def clean_info():
    f = open('poc_info.txt', 'w')
    info = generate_info(info_temp, info_words)
    print info
    f.write(info.encode('utf-8'))
    f.close()
    print '[+] poc_info cleared.'


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        check_site(url)

    clean_info()

if __name__ == "__main__":
    main()
 
