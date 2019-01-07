# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

def operate_factory(char):
    return operate_map.get(char)

operate_map = dict()

class MyMeta(type):
    def __init__(self, cls_name, cls_bases, cls_dict):
        super().__init__(self)

        if self.__name__ != 'BaseOperator':
            operate_map[self.name] = self

class BaseOperator(object, metaclass=MyMeta):
    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

        self.result = None
        self.cal()

    def cal(self):
        raise NotImplementedError('必须实现此方法')

# 加法
class Add(BaseOperator):
    name = '+'
    def cal(self):
        self.result = self.a + self.b


# # 减法
class Sub(BaseOperator):
    name = '-'
    def cal(self):
        self.result = self.a - self.b


# # 乘法
class Multi(BaseOperator):
    name = '*'
    def cal(self):
        self.result = self.a * self.b


# # 除法
class Div(BaseOperator):
    name = '/'
    def cal(self):
        self.result = self.a / self.b





if __name__ == '__main__':
    print(operate_map)
