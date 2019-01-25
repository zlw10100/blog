# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""迭代器模块
此模块定义了迭代器的行为。
"""


from abc import ABCMeta, abstractmethod


class AbstractIterator(object, metaclass=ABCMeta):
    @abstractmethod
    def first(self): pass

    @abstractmethod
    def next(self): pass

    @abstractmethod
    def is_done(self): pass

    @abstractmethod
    def cur_item(self): pass


class MyIterator(AbstractIterator):
    def __init__(self, set_object):
        self.set_object = set_object
        self.cur_index = 0

    def first(self):
        return self.set_object[0]

    def next(self):
        if not self.is_done:
            self.cur_index += 1
            return self.set_object[self.cur_index]

    @property
    def is_done(self):
        return self.cur_index == self.set_object.size - 1

    def cur_item(self):
        return self.set_object[self.cur_index]
