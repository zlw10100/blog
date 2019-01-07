# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


# Policy既是工厂也是策略容器类
from src.policys import Policy


price_list = [233,45,214,876]


def make_bill():
    final_price = 0
    
    # 所有的价格都是8折
    for price in price_list:
        policy = Policy('discount', 0.85)
        price = policy.cal(price)
        final_price += price
    print('最终价格是:', final_price)

if __name__ == '__main__':
    make_bill()












