# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""组件模块
此模块定义了组合模式的两个重要对象：组合对象(树枝节点)和单点对象(叶子节点)
"""


from abc import ABCMeta, abstractmethod

class AbstractComponent(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def add(self, c): pass

    @abstractmethod
    def remove(self, c): pass

    @abstractmethod
    def display(self, level): pass


# 单点对象(叶子节点)
class Leave(AbstractComponent):
    def add(self, c):
        print('叶子节点没有子节点')

    def remove(self, c):
        print('叶子节点没有子节点')

    def display(self, level):
        print('=' * level, self.name, type(self).__name__)


# 组合对象(树枝节点)
class Composite(AbstractComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children_list = list()  # 树枝节点有子节点列表

    def add(self, c):
        self.children_list.append(c)

    def remove(self, c):
        self.children_list.remove(c)

    # 树枝节点要迭代显示
    def display(self, level):
        print('=' * level, self.name, type(self).__name__)
        for children in self.children_list:
            children.display(level + 1)
