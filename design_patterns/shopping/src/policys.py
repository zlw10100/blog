# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


class PolicyContext(object):
    def __init__(self, instance):
        self.instance = instance

    def cal(self, price):
        return self.instance.cal(price)
# =============================================

class BasePolicy(object):
    def cal(self):
        raise NotImplementedError('必须被实现')

class CommonPolicy(BasePolicy):
    name = 'common' # 正常收银

    def cal(self, price):
        print('检测价格，返回原始价格')
        return price

class DiscountPolicy(BasePolicy):
    name = 'discount' # 打折优惠
    
    def __init__(self, discount):
        self.discount = discount

    def cal(self, price):
        print('检测价格，返回打折价格')
        return self.discount * price


class ReductionPolicy(BasePolicy):
    name = 'reduction'
    
    # 满减优惠
    def __init__(self, full, reduction):
        self.full = full
        self.reduction = reduction
    
    def cal(self, price):
        if price >= self.full:
            print('检测价格，返回满减价格')
            return price - self.reduction
        print('检测价格，未达满减要求')
        return price









