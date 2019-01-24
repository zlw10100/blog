# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""职责对象模块
此模块定义职责对象，这些对象需要被加入一个职责链中以便按照顺序处理事务。
"""


from abc import ABCMeta, abstractmethod


class AbstractManager(object, metaclass=ABCMeta):
    def set_boss(self, boss):
        self.boss = boss

    @abstractmethod
    def handle(self, event): pass


class CompanyManager(AbstractManager):
    def handle(self, event):
        if event.money < 10000:
            print('总经理审批ok')
        else:
            print('总经理不同意')


class DepartManager(AbstractManager):
    def handle(self, event):
        if event.money < 5000:
            print('部门经理审批ok')
        else:
            print('部门经理无权限，升级处理')
            return self.boss.handle(event)


class ProjectManager(AbstractManager):
    def handle(self, event):
        if event.money < 2000:
            print('项目经理经理审批ok')
        else:
            print('项目经理经理无权限，升级处理')
            return self.boss.handle(event)
