# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



class ObjectStructure(object):
    # 一个存放元素的列表，后续用于枚举
    element_list = list()

    # 增加元素对象
    def attach(self, element):
        self.element_list.append(element)

    # 移除元素对象
    def detach(self, element):
        self.element_list.remove(element)

    # 展示某一个算法对所有元素对象访问的结果
    def accept(self, visitor):
        for element in self.element_list:
            element.accept(visitor)








