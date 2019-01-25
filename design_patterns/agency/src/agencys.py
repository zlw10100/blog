# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""中介模块
此模块定义了中介的行为。
"""


from abc import ABCMeta, abstractmethod


class AbstractAgency(object, metaclass=ABCMeta):
    def __init__(self):
        self.customer_list = list()

    @abstractmethod
    def add(self, customer): pass

    @abstractmethod
    def publish(self, *args, **kwargs): pass


class UN(AbstractAgency):
    def add(self, customer):  # 为中介的客户清单中新增一个客户
        self.customer_list.append(customer)
        customer.connect(self)  # 设置此客户的连接接口

    def publish(self, msg):  # 向客户公布信息
        for customer in self.customer_list:
            customer.callback(
                origin='un',
                to='all country',
                msg=msg,
            )

    def transmit(self, origin, to, *args, **kwargs):  # 转发客户之间的单点信息
        kwargs.update({
            'origin': origin,
            'to': to,
        })
        to.callback(*args, **kwargs)
