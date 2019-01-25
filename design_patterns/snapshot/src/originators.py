# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""发起人模块
此模块定义了需要保留快照的发起人对象。
发起人实现了发起人接口，此接口要求发起人实现保留状态和设置状态。
"""


class OriginatorInterface(object):
    def save_state(self, snapshot_cls):
        pass

    def set_state(self, snapshot):
        pass


class GameOriginator(OriginatorInterface):
    def __init__(self, life_value, money):
        self.life_value = life_value
        self.money = money

    def attack_boss(self):
        self.life_value -= 23
        self.money -= 5000

    @property
    def info(self):
        return self.life_value, self.money

    def save_state(self, snapshot_cls):
        return snapshot_cls(self.life_value, self.money)

    def set_state(self, snapshot):
        self.life_value = snapshot.life_value
        self.money = snapshot.money
