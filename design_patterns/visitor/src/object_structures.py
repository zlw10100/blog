# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""对象结构模块
此模块定义了对象结构
"""


class ObjectStructureInterface(object):
    def add(self, element):
        raise NotImplementedError

    def remove(self, element):
        raise NotImplementedError

    def accept(self, visitor):
        raise NotImplementedError


# 对象结构，用于存放元素对象，且负责帮助算法遍历元素对象
class AccountBook(ObjectStructureInterface):
    element_list = list()

    # 增加元素对象
    def add(self, element):
        self.element_list.append(element)

    # 移除元素对象
    def remove(self, element):
        self.element_list.remove(element)

    # 展示某一个算法对所有元素对象访问的结果
    def accept(self, visitor):
        for element in self.element_list:
            element.accept(visitor)
