poc maker
===========

    poc 模板生成工具

### Help
    Usage: python poc_maker.py

### Example
* poc_info.txt填入info
* python poc_maker.py
* 可以用clean_info.py ,清空poc_info.txt,避免忘记修改某些...
* report_maker.py 生成周报


### Other
* template 涉及公司代码, 暂缺

### Changelog
* 1.根据poc_info信息填入必需的繁琐信息表格
* 2.文件及目录名的命名规则较繁琐,故一并生成,doc文件为读取xml修改节点,py文件为关键字替换
* 3.增加clea_info.py,用于清空poc_info.txt,避免忘记修改某些条目
* 4.clea_info.py 新增从wooyun url提取几条信息(有限信息,正在进行...)
* 5.增加weekdays.py 用于生成工作日期(poc_maker.py使用weekdays生成日期目录)
* 6.增加report_maker.py 用于生成周报(通过日期目录下的poc信息)

