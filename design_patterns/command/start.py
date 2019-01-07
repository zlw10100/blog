# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'




from src.persons import Person
from src.admin import Admin
from src.commands import DirCommand



if __name__ == '__main__':
    p = Person()
    print(p.is_executed)
    # 关联命令对象和接收者对象
    dir = DirCommand(p)

    # 实例化管理者对象
    # 管理者用于控制、管理、记录命令执行
    admin = Admin()
    # 设置一个要执行的命令对象
    admin.set_command(dir)
    # 执行命令
    admin.execute_command()
    print(p.is_executed)































