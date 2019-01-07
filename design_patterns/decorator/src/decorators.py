# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import abstractmethod
from src.compoent import AbstractFunction

# 装饰抽象类应该继承产品抽象类，以获得产品抽象类的接口并实现
# 这样才能表现的像实际的产品类
class AbstractDecorator(AbstractFunction):
    # 这里出现了抽象类继承抽象类的情况
    
    def __init__(self, function):
        # 指定一个引用，指向产品具体对象
        self.function = function
    
    # 定义抽象装饰类自有的接口
    @abstractmethod
    def get_real_object(self):pass


# 日志记录装饰类，增加日志记录功能
class LogDecorator(AbstractDecorator):
    # 要实现产品抽象类的接口
    def call(self):
        self.log()
        return self.function.call()

    # 也要实现装饰抽象类的接口
    def get_real_object(self):
        return self.function
    
    # 定义装饰模式提供的额外功能
    def log(self):
        print(f'{self.function}被调用，已记录日志')








