# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""软件模块
此模块定义了各种软件。
"""


from abc import ABCMeta, abstractmethod


class AbstractSoftWare(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def run(self):
        pass
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__


class ChatSoft(AbstractSoftWare):
    def run(self):
        print('聊天软件运行')


class VideoSoft(AbstractSoftWare):
    def run(self):
        print('视频软件运行')


class MusicSoft(AbstractSoftWare):
    def run(self):
        print('音乐软件运行')
