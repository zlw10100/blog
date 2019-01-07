# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


# 命令调用者，要设置回调函数访问命令执行完毕后的结果
class Person(object):
    def __init__(self):
        self.is_executed = False

    # 设置回调函数，当命令执行完毕的时候会执行此函数逻辑
    def callback(self, result):
        print('说明命令已经执行完毕,结果是:', result)
        self.is_executed = True










