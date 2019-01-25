# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""快照模块
此模块定义了快照的数据结构。
"""


class BaseSnapshot(object):
    pass


class GameSnapshot(BaseSnapshot):
    def __init__(self, life_value, money):
        self.life_value = life_value
        self.money = money
