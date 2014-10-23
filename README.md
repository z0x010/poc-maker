poc maker
===========

    poc 模板生成工具

### Help

    python poc_maker.py

    python poc_maker.py --report



    python poc_clean_info.py -h
    -h, --help            show this help message and exit
    -u VULURL, --vulurl VULURL Vulnerability Refer url eg. -u http://wooyun.org/bugs/wooyun-2014-073369
    -t VULTYPE, --vultype VULTYPE Vulnerability Type eg. -t sqli
    -i VULID, --vulid VULID Vulnerability ID eg. -i 111 id自动补全4位,变为0111
    -o VULTOOL, --vultool VULTOOL tools eg.sqlmap or Firefox
    -s VULDESC, --vuldesc VULDESC Vulnerability description
    -n APPNAME, --appname APPNAME app name eg. wordpress

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

    [+] finished clean.


### Example
* poc_info.txt填入info
* python poc_maker.py
* poc_maker.py 会自动生成本周日期目录
* python pocmaker.py --report 会根据本周日期目录下poc生成周报
* poc_clean_info.py ,清空poc_info.txt,避免忘记修改某些(无参数默认清空,参数-u根据url读取基本信息
,如-u http://wooyun.org/bugs/wooyun-2014-073369 也可指定参数修改info)



### Other
* template 涉及公司代码, 暂缺


### Changelog
* 1.根据poc_info信息填入必需的繁琐信息表格
* 2.文件及目录名的命名规则较繁琐,故一并生成,doc文件为读取xml修改节点,py文件为关键字替换
* 3.增加clea_info.py,用于清空poc_info.txt,避免忘记修改某些条目
* 4.clea_info.py 新增从wooyun url提取几条信息(有限信息,正在进行...)
* 5.增加weekdays.py 用于生成工作日期(poc_maker.py使用weekdays生成日期目录)
* 6.增加report_maker.py 用于生成周报(通过日期目录下的poc信息)
* 7.增加支持新框架模板(new_poc_template)
* 8.poc_clean_info.py 增加参数,无法自动读取时手动指定,主要用于修改默认tools及vultype
* 9.增加utils目录
* 10.poc_maker.py增加--report
