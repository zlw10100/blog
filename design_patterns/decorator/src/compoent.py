# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractFunction(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def call(self): pass
    
    def __str__(self):
        return f'<函数:{self.name}>'
    
    __repr__ = __str__


class SimpleFunction(AbstractFunction):
    def call(self):
        print('简单函数被调用,执行函数体定义的内容')










