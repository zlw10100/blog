# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""命令模块
此模块定义各种命令类。
"""


from abc import ABCMeta, abstractmethod


class AbstractCommand(object, metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


class DirCommand(AbstractCommand):
    command = 'dir'

    def execute(self):
        print(f'执行{self.command}方法')
        result = 'dir results is xxxxxx'
        status = True
        return status, result
