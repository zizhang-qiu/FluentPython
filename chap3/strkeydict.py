#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:qzz
@file:strkeydict.py
@time:2022/07/13
"""
import collections


class StrKeyDict(collections.UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


