# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.compoent import SimpleFunction
from src.decorators import LogDecorator


if __name__ == '__main__':
    # 实例化一个产品类对象
    func = SimpleFunction('执行科学计算')

    # 实例化一个装饰对象
    log_decorator = LogDecorator(func)

    # 将原有引用指向装饰后的对象
    func = log_decorator

    # func现在是指向一个装饰对象
    # 但是此装饰对象的接口与真正的func对象一样
    # 此外还提供了额外的日志记录功能
    func.call()

    # 装饰对象可以返回被装饰的对象
    print(func.get_real_object())
    








