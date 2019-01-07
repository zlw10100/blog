# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractOperate(object, metaclass=ABCMeta):
    @abstractmethod
    def handle(self, a, b):
        pass


class Add(AbstractOperate):
    def handle(self, a, b):
        return a + b
    
class Division(AbstractOperate):
    def handle(self, a, b):
        if b == 0:
            raise ZeroDivisionError('除0错误')
        return a / b









