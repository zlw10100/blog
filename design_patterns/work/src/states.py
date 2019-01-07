# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractState(object, metaclass=ABCMeta):
    @abstractmethod
    def work(self, w): pass


class MorningState(AbstractState):
    def work(self, w):
        if w.cur_hour < 12:
            print('在早上执行工作, 精神不错')
        else:
            # 不是当前状态，交给下一个状态管理
            w.set_state(AfterNoonState())
            w.work()


class AfterNoonState(AbstractState):
    def work(self, w):
        if 12 < w.cur_hour < 18:
            print('在下午执行工作, 有点迷糊')
        else:
            # 不是当前状态，交给下一个状态管理
            w.set_state(EveningState())
            w.work()


class EveningState(AbstractState):
    def work(self, w):
        if 18 < w.cur_hour:
            print('在晚上执行工作, 昏昏欲睡')
        else:
            # 不是当前状态，交给下一个状态管理
            w.set_state(MorningState())
            w.work()


