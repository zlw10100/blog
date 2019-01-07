# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from abc import ABCMeta, abstractmethod

class AbstractCommand(object, metaclass=ABCMeta):
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


# 具体的命令类
class DirCommand(AbstractCommand):
    def execute(self):
        print('执行dir方法')
        result = '命令执行结果'
        # 执行完后把结果发送给调用者的回调函数
        self.receiver.callback(result)


