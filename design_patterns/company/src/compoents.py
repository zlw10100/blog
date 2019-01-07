# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from abc import ABCMeta, abstractmethod

class Component(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def add(self, c): pass

    @abstractmethod
    def remove(self, c): pass

    @abstractmethod
    def display(self, level): pass


class Leave(Component):
    def add(self, c): print('叶子节点没有子节点')

    def remove(self, c): print('叶子节点没有子节点')

    def display(self, level): print('=' * level, self.name, type(self).__name__)


class Composite(Component):
    def __init__(self, name):
        super().__init__(name)
        self.children_list = list()

    def add(self, c): self.children_list.append(c)

    def remove(self, c): self.children_list.remove(c)

    # 树枝节点要迭代
    def display(self, level):
        print('=' * level, self.name, type(self).__name__)
        for children in self.children_list:
            children.display(level + 1)














