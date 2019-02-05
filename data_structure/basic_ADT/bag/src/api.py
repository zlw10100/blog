# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


# 第一步，定义api
"""
背包api的定义。
一个集合类的抽象数据类型，只能加入元素，但无法删除元素。

class Bag:
    Bag()           实例化一个背包对象
    
    void add(item)  向背包中加入一个元素
    bool is_empty() 判断背包是否为空
    int size()      获取当前背包的容量大小
    __iter__        生成当前背包的迭代器对象
    __next__        获取当前背包中的下一个元素
    iter_item       将背包中的数据迭代成列表输出
"""


from abc import ABCMeta, abstractmethod


class IteratorInterface(object):
    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class AbstractBag(IteratorInterface, metaclass=ABCMeta):
    """抽象背包类接口"""

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass
