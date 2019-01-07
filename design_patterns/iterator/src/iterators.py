# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'





from abc import ABCMeta, abstractmethod

class Iterator(object, metaclass=ABCMeta):
    @abstractmethod
    def first(self): pass

    @abstractmethod
    def next(self): pass

    @abstractmethod
    def is_done(self): pass

    @abstractmethod
    def cur_item(self): pass

class MyIterator(Iterator):
    def __init__(self, object_set):
        self.object_set = object_set
        self.cur_index = 0

    def first(self): return self.object_set[0]

    def next(self):
        if not self.is_done:
            self.cur_index += 1
            return self.object_set[self.cur_index]

    @property
    def is_done(self):
        if self.cur_index == self.object_set.size - 1:
            return True
        return False

    def cur_item(self):
        return self.object_set[self.cur_index]








