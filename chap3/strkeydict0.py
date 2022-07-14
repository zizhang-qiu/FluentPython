#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:qzz
@file:strkeydict0.py
@time:2022/07/13
"""


class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()