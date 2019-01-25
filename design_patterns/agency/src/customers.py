# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""客户类模块
此模块定义了各种客户类，
每一个客户类都会被要求连接到中介，
每一个客户类被要求实现一个回调函数。
每一个客户类被要求实现一个消息发送函数。
"""


from abc import ABCMeta, abstractmethod


class AbstractCustomer(object, metaclass=ABCMeta):
    def __init__(self):
        self.agency = None

    def connect(self, agency):
        self.agency = agency

    @abstractmethod
    def callback(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, target, *args, **kwargs):
        pass


class Country(AbstractCustomer):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def callback(self, *args, **kwargs):
        print(f'{self.name}收到新的消息是: ', args, kwargs)

    def send(self, target, *args, **kwargs):
        self.agency.transmit(self, target, *args, **kwargs)

    def __str__(self):
        return self.name

    __repr__ = __str__

