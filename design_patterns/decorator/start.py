# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的装饰模式的实现程序
为一个简单的函数调用封装额外的日志统计功能。
装饰模式就是在某一个真实组件对象的基础上增加额外的功能。
"""


from src.products import ProductFunc
from src.decorators import LogDecorator


if __name__ == '__main__':
    # 实例化一个产品类对象
    func = ProductFunc('科学计算函数')

    # 实例化一个装饰对象
    log_decorator = LogDecorator(func)
    print(func is log_decorator.get_real_object())  # True, 装饰对象里有一个真实对象的引用

    # 将原有引用指向装饰后的对象
    func = log_decorator

    # func现在是指向一个装饰对象
    # 但是此装饰对象的接口与真正的func对象一样
    # 此外还提供了额外的日志记录功能
    func.call()
    # < 函数: 科学计算函数 > 被调用，已记录日志
    # 简单函数被调用, 执行函数体定义的内容

    # 装饰对象可以返回被装饰的对象
    print(func.get_real_object())
    # < 函数: 科学计算函数 > 
