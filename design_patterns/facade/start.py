# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现外观模式的程序
模拟投资理财的途径，使用一个基金经理帮助大众打理各种具体的理财细节。
"""


from src.fund_managers import FundA


if __name__ == '__main__':
    fund_a = FundA()  # 基金为客户提供了一个简单的外观接口

    fund_a.buy()  # 客户不再需要将每一种理财方式都购买一遍
    # 基金经理A开始帮助客户理财，准备买入一些资产
    # 购买黄金
    # 购买债券

    fund_a.sell()  # 客户也不再需要把所有的理财方式都出售一遍
    # 基金经理A开始帮助客户理财，准备卖出一些资产
    # 出售黄金
    # 出售债券
