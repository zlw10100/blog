# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""集合模块
此模块定义了集合对象。
"""


from src.iterators import MyIterator


class SetInterface(object):
    def create_iterator(self):
        raise NotImplementedError


class MySet(SetInterface):
    def __init__(self, *list):
        self._list = list
        self.size = len(list)

    # 为集合对象创建一个迭代器对象，迭代器对象有一个引用指向集合对象
    def create_iterator(self):
        return MyIterator(self)

    # 模拟数组取值
    def __getitem__(self, item):
        return self._list[item]
