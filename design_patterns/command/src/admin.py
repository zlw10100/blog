# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'






# 管理者，负责管理命令记录
class Admin(object):
    def __init__(self):
        # 保留命令以备后续使用
        self.command_list = list()
        
    def set_command(self, command):
        self.cur_command = command
        self.command_list.append(command)

    # 由实际的命令对象来执行
    def execute_command(self):
        self.cur_command.execute()










