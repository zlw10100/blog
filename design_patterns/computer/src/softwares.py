# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class SoftWare(object, metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def run(self):
        pass
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__


class ChatSoft(SoftWare):
    def run(self):
        print('聊天软件运行')


class VideoSoft(SoftWare):
    def run(self):
        print('视频软件运行')


class MusicSoft(SoftWare):
    def run(self):
        print('音乐软件运行')





