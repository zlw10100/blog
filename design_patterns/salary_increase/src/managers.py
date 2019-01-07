# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractLeader(object, metaclass=ABCMeta):
    def set_boss(self, boss):
        self.boss = boss

    @abstractmethod
    def handle(self, event): pass

class CompanyManager(AbstractLeader):
    def handle(self, event):
        if event.money < 10000:
            print('总经理审批ok')
        else:
            print('总经理不同意')

class DepartManager(AbstractLeader):
    def handle(self, event):
        if event.money < 5000:
            print('部门经理审批ok')
        else:
            print('部门经理无权限，升级处理')
            return self.boss.handle(event)

class ProjectManager(AbstractLeader):
    def handle(self, event):
        if event.money < 2000:
            print('项目经理经理审批ok')
        else:
            print('项目经理经理无权限，升级处理')
            return self.boss.handle(event)


