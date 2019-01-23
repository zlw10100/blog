# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""真实产品对象(业务类)模块
此模块中的真实产品是一个函数。
"""


from abc import ABCMeta, abstractmethod


class AbstractProduct(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def call(self): pass
    
    def __str__(self):
        return f'<函数:{self.name}>'
    
    __repr__ = __str__


class ProductFunc(AbstractProduct):
    def call(self):
        print('简单函数被调用,执行函数体定义的内容')
