# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.callers import CmdCaller
from src.managers import CmdManager
from src.commands import DirCommand


if __name__ == '__main__':
    # 实例化命令
    dir_obj = DirCommand()

    # 实例化命令管理者
    cmd_manager = CmdManager()

    # 装配命令
    cmd_manager.save(dir_obj.command, dir_obj)

    # 实例化调用者
    caller = CmdCaller(manager=cmd_manager)

    # 调用命令
    caller.execute('dir')
    # 执行dir方法
    # 命令执行成功
    # 结果是: dir
    # results is xxxxxx
