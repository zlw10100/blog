# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""调用者模块"""


class CmdCaller(object):
    def __init__(self, manager):
        self.manager = manager

    def execute(self, command, *args, **kwargs):
        self.manager.execute(self, command, *args, **kwargs)

    def callback(self, status, result):
        if status is True:
            print('命令执行成功')
            print('结果是:', result)
        else:
            print('命令执行失败')
            print('失败原因是:', result)
