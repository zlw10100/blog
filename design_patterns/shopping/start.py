# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.policys import (
    PolicyContext,  # 需要维护策略上下文类
    CommonPolicy,  # 需要维护所有使用的具体策略类
    DiscountPolicy,
    ReductionPolicy,
)


price_list = [233,45,214,876]


def make_bill():
    final_price = 0
    
    # 所有的价格都是8折
    for price in price_list:
        policy = PolicyContext(DiscountPolicy(0.8))
        price = policy.cal(price)
        final_price += price
    print('最终价格是:', final_price)

if __name__ == '__main__':
    make_bill()












