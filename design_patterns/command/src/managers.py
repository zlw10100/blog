# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""命令管理者模块
此模块与命令对象以及调用者对象双向依赖。
此模块管理调用者对象的调用操作，比如：身份验证、权限判定、回调结果等。
此模块管理命令对象的执行操作，比如：存储命令对象、调用命令，获取结果等。
"""


class CmdManager(object):
    # cmd命令存储字典: command -> command_obj
    command_map = dict()

    def save(self, command, command_obj):
        self.command_map[command] = command_obj

    # 由实际的命令对象来执行
    def execute(self, caller, command, *args, **kwargs):
        command_obj = self.command_map.get(command)
        status, result = command_obj.execute(*args, **kwargs)
        caller.callback(status, result)
