# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""策略模块
此模块定义了各种策略类。
"""


class BasePolicy(object):
    pass


# 价格策略基类
class BasePricePolicy(BasePolicy):
    pass


# 普通价格策略类
class CommonPricePolicy(BasePricePolicy):
    name = 'common' # 正常收银

    def calculate(self, price):
        print('检测价格，返回原始价格')
        return price


class DiscountPricePolicy(BasePricePolicy):
    name = 'discount' # 打折优惠
    
    def __init__(self, discount):
        self.discount = discount

    def calculate(self, price):
        print('检测价格，返回打折价格')
        return self.discount * price


class ReductionPricePolicy(BasePricePolicy):
    name = 'reduction'  # 满减优惠

    def __init__(self, full, reduction):
        self.full = full
        self.reduction = reduction
    
    def calculate(self, price):
        if price >= self.full:
            print('检测价格，返回满减价格')
            return price - self.reduction
        print('检测价格，未达满减要求')
        return price
