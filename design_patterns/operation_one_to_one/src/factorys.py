# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

from src.operates import (
    Add,
    Division,
)

class AbstractFactory(object, metaclass=ABCMeta):
    @abstractmethod
    def create_operate(self):
        pass



class AddFactory(AbstractFactory):
    def create_operate(self):
        return Add()
    
class DivisionFactory(AbstractFactory):
    def create_operate(self):
        return Division()







