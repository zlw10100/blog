# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现策略模式的程序
此程序模拟账单结账时，不同策略会产生不同的结账金额。
"""


from src.contexts import PricePolicyContext  # 策略容器类

from src.policys import (  # 策略类
    CommonPricePolicy,
    DiscountPricePolicy,
    ReductionPricePolicy,
)


if __name__ == '__main__':
    # 定义价格清单
    price_list = [233,45,214,876]

    # 最终价格
    final_price = 0

    # 策略1: 打折策略，所有的价格都是8折
    context = PricePolicyContext(DiscountPricePolicy(0.8))  # 装配策略
    for price in price_list:
        final_price += context.handle(price)
    print('最终价格是:', final_price)
    # 检测价格，返回打折价格
    # 检测价格，返回打折价格
    # 检测价格，返回打折价格
    # 检测价格，返回打折价格
    # 最终价格是: 1094.4


    # 策略2: 满减策略，满230就减50
    context = PricePolicyContext(ReductionPricePolicy(230, 50))  # 装配策略
    for price in price_list:
        final_price += context.handle(price)
    print('最终价格是:', final_price)
    # 检测价格，返回满减价格
    # 检测价格，未达满减要求
    # 检测价格，未达满减要求
    # 检测价格，返回满减价格
    # 最终价格是: 2362.4
