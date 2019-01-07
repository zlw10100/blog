# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'




from abc import ABCMeta, abstractmethod

# 访问者类代表着对数据的操作
class AbstractVisitor(object, metaclass=ABCMeta):
    # 因为男人女人这个结构是稳定的
    # 所以访问者抽象类中的抽象方法个数也是稳定的
    @abstractmethod
    def visitor_man(self, man):
        pass

    @abstractmethod
    def visitor_woman(self, woman):
        pass


# 可以认为是算法类，定义对稳定的数据结构的算法逻辑操作
class HandleA(AbstractVisitor):
    # 定义算法/操作/处理对象类A对男人数据的访问逻辑
    def visitor_man(self, man):
        print('当前是算法A，准备对男人数据执行操作')

    # 定义算法/操作/处理对象类A对女人数据的访问逻辑
    def visitor_woman(self, woman):
        print('当前是算法A，准备对女人数据执行操作')


class HandleB(AbstractVisitor):
    # 定义算法/操作/处理对象类B对男人数据的访问逻辑
    def visitor_man(self, man):
        print('当前是算法B，准备对男人数据执行操作')

    # 定义算法/操作/处理对象类B对女人数据的访问逻辑
    def visitor_woman(self, woman):
        print('当前是算法B，准备对女人数据执行操作')





