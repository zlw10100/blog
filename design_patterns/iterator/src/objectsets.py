# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""集合模块
此模块定义了集合对象。
"""


from abc import ABCMeta, abstractmethod
from src.iterators import MyIterator


class SetInterface(object):
    def create_iterator(self):
        raise NotImplementedError


class MySet(SetInterface):
    def __init__(self, *list):
        self._list = list
        self.size = len(list)

    def create_iterator(self):
        return MyIterator(self)

    def __getitem__(self, item):
        return self._list[item]










