# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from abc import ABCMeta, abstractmethod


class AbstractCountry(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        self.agency = None

    @abstractmethod
    def new_msg(self, msg): pass


class Country(AbstractCountry):
    def connect(self, agency):
        self.agency = agency

    def new_msg(self, msg):
        print(f'{self.name}收到新的消息是: {msg}')



