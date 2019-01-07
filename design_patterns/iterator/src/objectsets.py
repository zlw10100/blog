# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'




from abc import ABCMeta, abstractmethod
from src.iterators import MyIterator

class ObjectSet(object, metaclass=ABCMeta):
    @abstractmethod
    def create_iterator(self): pass


class MySet(ObjectSet):
    def __init__(self, *list):
        self._list = list
        self.size = len(list)

    def create_iterator(self):
        return MyIterator(self)

    def __getitem__(self, item):
        return self._list[item]










