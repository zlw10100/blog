# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""元素对象模块
此模块定义了各种元素对象。
"""


from abc import ABCMeta, abstractmethod


# 元素对象类代表着数据
class AbstractElement(object, metaclass=ABCMeta):
    # 每一个元素对象都需要接受一个访问者(算法对象)来操作自己
    @abstractmethod
    def accept(self, visitor):
        pass


# 具体的元素类
class Income(AbstractElement):
    name = '收入'

    def accept(self, visitor):
        # 接受一个算法的访问
        visitor.visit(self)


# 具体的元素类
class Pay(AbstractElement):
    name = '支出'

    def accept(self, visitor):
        # 接受一个算法的访问
        visitor.visit(self)
