# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""访问者模块
此模块定义了访问者的行为。
"""


# 访问者类代表着算法对象
class VisitorInterface(object):
    def visit(self, element):
        raise NotImplementedError


class Boss(VisitorInterface):
    def visit(self, element):
        print('老板查看', element.name, '主要查看利润数据')


class Manager(VisitorInterface):
    def visit(self, element):
        print('经理查看', element.name, '主要查看成本数据')


class Cashier(VisitorInterface):
    def visit(self, element):
        print('出纳查看', element.name, '主要查看流水数据')
