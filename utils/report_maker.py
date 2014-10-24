#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from weekdays import weekdays

MYNAME = '[flsf]'


def make_report():
    dirname = weekdays()
    report_name = '[周报]' + MYNAME + dirname.replace(':', '/')
    pocs = []
    if os.path.exists(dirname):
        pocs = os.listdir(dirname)
    else:
        print '[-] {dirname} is not exist'.format(dirname=dirname)
        sys.exit(0)

    try:
        pocs.remove('.DS_Store')
    except Exception,e:
        pass

    week_job = ['\n本周工作\n']
    for index, pocname in enumerate(pocs):
        week_job.append(str(index + 1) + '.' + pocname + ' POC+文档  [已经完成]\n')

    week_job.append('\n\n下周工作\n继续wsl工作')
    week_job.append('\n\n唧唧歪歪')

    report = report_name + '\n'
    for _ in week_job:
        report += _

    print report

    report_file = open(report_name.replace('/', ':') + '.txt', 'w')
    report_file.write(report)


def main():
    make_report()

if __name__ == '__main__':
    main()
