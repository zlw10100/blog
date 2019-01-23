# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""装饰模块"""


from abc import abstractmethod

from src.products import AbstractProduct  # 引入被装饰的真实业务类


# 装饰抽象类应该继承产品抽象类，以获得产品抽象类的接口并实现，这样才能表现的像实际的产品类
class AbstractDecorator(AbstractProduct):  # 这里出现了抽象类继承抽象类的情况
    def __init__(self, product):
        # 指定一个引用，指向产品具体对象
        self.product = product
    
    # 定义抽象装饰类自有的接口
    @abstractmethod
    def get_real_object(self):pass


# 日志记录装饰类，为产品增加日志记录功能
class LogDecorator(AbstractDecorator):
    # 定义装饰模式提供的额外功能
    def log(self):
        print(f'{self.product}被调用，已记录日志')
        
    # 要实现产品抽象类的接口
    def call(self):
        self.log()
        return self.product.call()  # 依然返回真实产品对象的执行结果

    # 也要实现装饰抽象类的接口
    def get_real_object(self):
        return self.product
