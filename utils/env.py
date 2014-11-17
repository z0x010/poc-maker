#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def module_path():
    _ = __file__
    utils_path = os.path.dirname(os.path.realpath(get_unioncode(_, sys.getfilesystemencoding())))
    return os.path.abspath(os.path.join(utils_path, '..'))


def poc_info_path():
    return os.path.join(paths.ROOT_PATH, 'poc_info.txt')


def doc_template_path():
    doc_template = os.path.join(paths.ROOT_PATH, 'template/poc_template.docx')
    return doc_template


def poc_template_path():
    poc_template = os.path.join(paths.ROOT_PATH, 'template/new_poc_template.txt')
    return poc_template


def comm_path():
    return os.path.join(paths.ROOT_PATH, 'template/comm')


def get_unioncode(value, encoding=None, noneToNull=False):
    if noneToNull and value is None:
        return NULL

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or kb.get("pageEncoding") or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")


def set_paths():
    paths.ROOT_PATH = module_path()
    paths.INFO_PATH = poc_info_path()
    paths.TEMPLATE_POC_PATH = poc_template_path()
    paths.TEMPLATE_DOC_PATH = doc_template_path()
    paths.COMM_PATH = comm_path()


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


class AttribDict(dict):
    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError, e:
            print e

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """

        # This test allows attributes to be set in the __init__ method
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # Any normal attributes are handled normally
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal

paths = AttribDict()
