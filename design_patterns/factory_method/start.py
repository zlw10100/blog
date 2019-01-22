# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的计算器程序
用户给定两个数字并指定对应计算的工厂类，由此工厂类生成操作符对象并执行计算。
"""


from src.factorys import (  # 用户自行选择指定的工厂类
    AddFactory,
    SubFactory,
    MultiFactory,
    DivisionFactory,
)


if __name__ == '__main__':
    x = 23
    y = 44
    add_factory = AddFactory()
    add = add_factory.create_operator(x, y)
    print(add.handle())  # 67

    x = 3
    y = 4
    sub_factory = SubFactory()
    sub = sub_factory.create_operator(x, y)
    print(sub.handle())  # -1

    x = 11
    y = 22
    multi_factory = MultiFactory()
    multi = multi_factory.create_operator(x, y)
    print(multi.handle())  # 242

    x = 100
    y = 0  # 会引发除0错误
    division_factory = DivisionFactory()
    division = division_factory.create_operator(x, y)
    print(division.handle())  # ZeroDivisionError
