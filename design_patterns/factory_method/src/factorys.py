# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""工厂模块
为每一个业务类编写一个工厂类以提供：实例化控制、封装。
工厂类与业务类为一对一映射关系。
"""


from abc import ABCMeta, abstractmethod

from src.operators import (
    Add,
    Sub,
    Multi,
    Division,
)


class AbstractFactory(object, metaclass=ABCMeta):
    """抽象工厂类"""
    
    @abstractmethod
    def create_operator(self, x, y):
        """每一个工厂类均提供此方法"""
        pass


class AddFactory(AbstractFactory):
    def create_operator(self, x, y):
        return Add(x, y)


class SubFactory(AbstractFactory):
    def create_operator(self, x, y):
        return Sub(x, y)
    
    
class MultiFactory(AbstractFactory):
    def create_operator(self, x, y):
        return Multi(x, y)
    
    
class DivisionFactory(AbstractFactory):
    def create_operator(self, x, y):
        # 可以做逻辑控制
        if y == 0:
            raise ZeroDivisionError
        return Division(x, y)
