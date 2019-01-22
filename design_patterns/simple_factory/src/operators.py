# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


operator_map = dict()


class AutoMappingMeta(type):
    """自动映射元类"""
    def __new__(cls, class_name, class_bases, class_dict):
        new_cls = super().__new__(cls, class_name, class_bases, class_dict)

        if new_cls.__name__ != 'BaseOperator':
            if not hasattr(new_cls, 'name'):
                raise RuntimeError(f'所有子类必须定义name属性')
            operator_map[getattr(new_cls, 'name')] = new_cls

        return new_cls


def operator_factory(char, *args, **kwargs):
    """简单工厂函数
    根据用户提供的输入，选择对应的类并返回一个实例化对象。
    """

    cls = operator_map.get(char)
    return cls(*args, **kwargs)


# 定义一个基类或者抽象类来统一控制所有的子类
class BaseOperator(object, metaclass=AutoMappingMeta):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.result = None

    def cal(self):
        raise NotImplementedError('必须实现此方法')


# 加法
class Add(BaseOperator):
    name = '+'

    def cal(self):
        self.result = self.x + self.y


# # 减法
class Sub(BaseOperator):
    name = '-'

    def cal(self):
        self.result = self.x - self.y


# # 乘法
class Multi(BaseOperator):
    name = '*'

    def cal(self):
        self.result = self.x * self.y


# # 除法
class Div(BaseOperator):
    name = '/'

    def cal(self):
        self.result = self.x / self.y
