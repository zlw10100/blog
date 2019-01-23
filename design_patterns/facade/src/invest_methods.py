# !/usr/bin/python
# -*- coding:utf-8 -*-


"""投资方法模块
此模块定义了各种投资方法。
"""


from abc import ABCMeta, abstractmethod


class AbstractInvestment(metaclass=ABCMeta):
    @abstractmethod
    def buy(self): pass  # 购买

    @abstractmethod
    def sell(self): pass  # 售卖


# 黄金投资
class Gold(AbstractInvestment):
    def buy(self):
        print('购买黄金')

    def sell(self):
        print('出售黄金')


# 债券投资
class Bond(AbstractInvestment):
    def buy(self):
        print('购买债券')

    def sell(self):
        print('出售债券')
