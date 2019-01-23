# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/23


"""基金经理模块
基金经理统一管理所有的理财方法，仅为客户开放购买基金和出售基金的接口。
客户不再需要了解每一种理财的具体方法，仅需要了解基金的使用接口即可。
"""


from abc import ABCMeta, abstractmethod

from src.invest_methods import (
    Gold,
    Bond,
)


class AbstractFund(metaclass=ABCMeta):
    @abstractmethod
    def buy(self): pass

    @abstractmethod
    def sell(self): pass


class FundA(AbstractFund):
    def buy(self):
        print('基金经理A开始帮助客户理财，准备买入一些资产')
        gold = Gold()
        gold.buy()

        bond = Bond()
        bond.buy()

    def sell(self):
        print('基金经理A开始帮助客户理财，准备卖出一些资产')
        gold = Gold()
        gold.sell()

        bond = Bond()
        bond.sell()
