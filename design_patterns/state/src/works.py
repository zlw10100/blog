# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""工作(业务)模块"""


from abc import ABCMeta, abstractmethod


class AbstractWork(object, metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, state):
        pass
    
    @abstractmethod
    def work(self):
        pass


class ProgramWork(AbstractWork):
    def __init__(self):
        self.cur_hour = None
        self.state = None
    
    def set_state(self, state):
        self.state = state
    
    def work(self): 
        self.state.work(self)
