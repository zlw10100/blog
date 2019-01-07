# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



class View():
    def view(self):
        # 向用户获取2个数字和运算符
        print('欢迎来到计算器')
        a = input('请输入第1个数字:')
        b = input('请输入第2个数字:')
        o = input('请输入操作符:')
        print(a, o, b)

        return a, b, o












