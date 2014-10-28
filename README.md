poc maker
===========

    poc 模板生成工具

### Help

    python poc_maker.py

    python poc_maker.py --report



    python poc_clean_info.py -h
    usage: poc_clean_info.py [-h] [-u VULURL] [-t VULTYPE] [-i VULID] [-o VULTOOL]
                             [-s VULDESC] [-n APPNAME] [--target-url TARGET_URL]
                             [--data DATA] [--test-url TEST_URL] [-m1 MATCH]
                             [-m2 MATCH_OTHER]

    optional arguments:
    -h, --help            show this help message and exit
    -u VULURL, --vulurl VULURL
                        Vulnerability Refer url eg. -u
                        http://wooyun.org/bugs/wooyun-2014-073369
    -t VULTYPE, --vultype VULTYPE
                        Vulnerability Type eg. -t sqli
    -i VULID, --vulid VULID
                        Vulnerability ID eg. -i 111
                        id自动补全4位,变为0111
    -o VULTOOL, --vultool VULTOOL
                        tools eg.sqlmap or Firefox
    -s VULDESC, --vuldesc VULDESC
                        Vulnerability description
    -n APPNAME, --appname APPNAME
                        APP name eg. wordpress
    -p VULPATH, --vulpath VULPATH
                        Vulnerability path eg. /index.php
    --target-url TARGET_URL
                        Vulnerability target url
    --data DATA           Post data
    --test-url TEST_URL   Vulnerability test site
    --appversion APPVERSION
                        APP version eg. 1.0
    -m1 MATCH, --match MATCH
                        Verify match
    -m2 MATCH_OTHER, --match-other MATCH_OTHER
                        Verify other match 



    python poc_clean_info.py -u http://wooyun.org/bugs/wooyun-2014-073369

    [*] read info from http://wooyun.org/bugs/wooyun-2014-073369
    appname    :=
    appversion :=
    appvendor  := http://www.hanweb.com

    vulid      :=
    vulpath    :=
    vultype    := SQL Injection
    vulreferer := http://wooyun.org/bugs/wooyun-2014-073369
    vuldesc    :=
    vuleffect  := SQL注入,泄露信息
    vuldate    := 2014-08-25


    tools      := Firefox
    tooldesc   := 浏览器

    myname     :=
    shortname  :=


    info_target_url :=
    info_post_data  :=
    info_match      :=
    info_ohter_match:=
    info_test_url   :=

    [+] finished clean.


### Example
* poc_info.txt填入info
* python poc_maker.py 根据poc_info生成poc模板,包括py文件及doc文档,同时生成本周工作日目录
* python pocmaker.py --report 会根据本周工作日目录下poc生成周报
* poc_clean_info.py ,清空poc_info.txt,避免忘记修改某些(无参数默认清空,参数-u根据url读取基本信息
,如-u http://wooyun.org/bugs/wooyun-2014-073369 也可指定参数修改info)
* poc_clean_info.py 可以指定taget-url, post-data, match, match_other,也可以根据poc_info.txt手动修改,会根据指定info自动调整模板



### Other
* template 涉及公司代码, 暂缺


### Changelog
* 1.根据poc_info信息填入必需的繁琐信息表格
* 2.文件及目录名的命名规则较繁琐,故一并生成,doc文件为读取xml修改节点,py文件为关键字替换
* 3.增加clea_info.py,用于清空poc_info.txt,避免忘记修改某些条目
* 4.clea_info.py 新增从wooyun url提取几条信息(有限信息,正在进行...)
* 5.增加weekdays.py 用于生成工作日期(poc_maker.py使用weekdays生成日期目录)
* 6.增加report_maker.py 用于生成周报(通过工作日目录下的poc信息)
* 7.增加支持新框架模板(new_poc_template)
* 8.poc_clean_info.py 增加参数,无法自动读取时手动指定,主要用于修改默认tools及vultype
* 9.增加utils目录
* 10.poc_maker.py增加--report
* 11.poc_clean_info.py 增加--target-url,--data,-m1,-m2,--test-url
* 12.增加utils/print_status.py 用于termcolor
