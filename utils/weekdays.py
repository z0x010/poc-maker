#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import calendar


def last_monday():
    last_monday = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while last_monday.weekday() != calendar.MONDAY:
        last_monday -= oneday
    return last_monday


def last_friday():
    last_friday = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while last_friday.weekday() != calendar.FRIDAY:
        last_friday -= oneday
    return last_friday


def next_friday():
    next_friday = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while next_friday.weekday() != calendar.FRIDAY:
        next_friday += oneday
    return next_friday


def weekdays():
    monday = last_monday()
    l_friday = last_friday()
    n_friday = next_friday()
    if monday > l_friday:
        friday = n_friday
    else:
        friday = l_friday
    return str(monday).replace('-', ':') + '-' + str(friday).replace('-', ':')  # ':' is '/'  mac os


def make_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def main():
    dirname = weekdays()
    print dirname
    make_dir(dirname)

if __name__ == '__main__':
    main()
