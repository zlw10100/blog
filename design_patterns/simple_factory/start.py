# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个非常简单的计算器程序
用户输入两个数字及一个操作符即可得到计算的结果。

源代码结构划分为：
1. 计算器的界面模块
2. 计算器的计算模块
3. 计算器的操作符模块，此模块使用简单工厂模式设计
"""


from src.calculate import cal
from src.view import view


def run():
    """计算器公开接口"""

    x, y, o = view()  # 获取界面并得到用户输入
    result = cal(x, y, o)  # 获取计算接口并得到结果
    print('结果是:', result)


if __name__ == '__main__':
    run()
    
    # 请输入第1个数字: 23
    # 请输入第2个数字: 2
    # 请输入操作符: +
    # 23 + 2
    # 结果是: 25
    # 
    # 请输入第1个数字: 55
    # 请输入第2个数字: 5
    # 请输入操作符: *
    # 55 * 5
    # 结果是: 275
