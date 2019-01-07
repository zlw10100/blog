# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from abc import ABCMeta, abstractmethod


class AbstractAgency(object, metaclass=ABCMeta):
    def __init__(self):
        self.customer_list = list()

    @abstractmethod
    def add_customer(self, c): pass

    @abstractmethod
    def send_all(self, msg): pass


class UN(AbstractAgency):
    def add_customer(self, c):
        # 中介的客户清单中新增一个客户
        self.customer_list.append(c)
        # 此客户联系到中介
        c.connect(self)

    def send_all(self, msg):
        for customer in self.customer_list:
            customer.new_msg(msg)



