# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""计算器的界面模块"""


def view():
    # 向用户获取2个数字和运算符
    print('欢迎来到xxx计算器')
    x = input('请输入第1个数字:')
    y = input('请输入第2个数字:')
    o = input('请输入操作符:')
    print(x, o, y)

    return x, y, o
