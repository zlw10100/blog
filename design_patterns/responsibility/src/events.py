# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""事件模块
此模块定义事件的具体属性和方法。
"""


class SalaryIncreaseEvent(object):
    def __init__(self, money):
        self.money = money
