# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.record import GameRecord


class Player(object):
    def __init__(self, name, aggrv, defined, life_value):
        self.name = name
        self.aggrv = aggrv
        self.defined = defined
        self.life_value = life_value

    def fight_boss(self):
        self.aggrv -= 12
        self.life_value -= 77
        self.defined -= 24

    def save_state(self):  # 定义存储的属性
        return GameRecord(
            self.aggrv,
            self.defined,
            self.life_value,
        )

    def set_state(self, record):  # 恢复存储的属性
        self.aggrv = record.aggrv
        self.defined = record.defined
        self.life_value = record.life_value

    def show_state(self):
        print('当前角色状态:', self.__dict__)









