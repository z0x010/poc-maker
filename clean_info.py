#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flsf 2014.9.22

import re
import sys
import urllib
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
TOOLS = u'sqlmap'
TOOLSDESC = u'SQL注入测试工具'
VULDATE = u'2014-09-'

info_words = {'vuldate': '', 'vuleffect': '', 'vultype': '', 'vulvendor': '', 'vuldesc': '', 'vulreferer': '', 'tools': TOOLS, 'toolsdesc': TOOLSDESC, 'myname': MYNAME, 'shortname': SHORTNAME}

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

sql_list = [u'SQL Injection', u'SQL注射']

def read_info_content(url):
    print '[*] read info from ' + url
    content = urllib.urlopen(url).read()
    soup = BeautifulSoup(content)
    info_list = soup.find("div", class_="content").find_all("h3")
    return info_list

def read_vultype(info):
    vultype = u''
    title_info = info[5].string
    for sql_key in sql_list:
        if sql_key in title_info:
            vultype = sql_list[0]
    return vultype

def read_vulvendor(info):
    vendor_info = info[2].a.get("href").encode("utf-8")
    content = urllib.urlopen(vendor_info).read()
    soup = BeautifulSoup(content)
    url_info = soup.find("div", class_="content").h3.string
    vulvendor = re.search('http.*', url_info).group(0)
    return vulvendor

def read_vuldate(info):
    date_info = info[4].string
    vuldate = re.search('20[1-2][3-9]-[0-9]+-[0-9]+', date_info).group(0)
    return vuldate

def read_vuleffect(vultype):
    if vultype == 'SQL Injection':
        vuleffect = u'SQL注入,泄露信息'
    return vuleffect

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        info = read_info_content(url)
        vultype = read_vultype(info)
        vulvendor = read_vulvendor(info)
        print vulvendor
        vuldate = read_vuldate(info)
        vuleffect = read_vuleffect(vultype)
        vulreferer = url
        info_words['vultype'] = vultype
        info_words['vulvendor'] = vulvendor
        info_words['vuldate'] = vuldate
        info_words['vulreferer'] = url
        info_words['vuleffect'] = vuleffect
    
    f = open('poc_info.txt', 'w')
    info = generate_info(info_temp, info_words)
    print info
    f.write(info.encode('utf-8'))
    f.close()
    print '[+] poc_info have cleared.'

if __name__ == "__main__":
    main()
 
