# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""上下文容器模块
此模块定义了上下文容器类的行为。
每一个容器类都要实现一个处理函数以执行当前装配的策略。
"""


from abc import ABCMeta, abstractmethod


class AbstractPolicyContext(object, metaclass=ABCMeta):
    @abstractmethod
    def handle(self, *args, **kwargs):
        pass


class PricePolicyContext(AbstractPolicyContext):
    def __init__(self, policy):
        self.policy = policy

    def handle(self, price):
        return self.policy.calculate(price)
