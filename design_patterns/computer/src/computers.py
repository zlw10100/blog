# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'




from abc import ABCMeta, abstractmethod

class Computer(object, metaclass=ABCMeta):
    def __init__(self):
        self.soft_list = list()
        
    @abstractmethod
    def set_software(self, s):
        pass

    def show_softwares(self):
        print(self.soft_list)

# 台式电脑
class DesktopComputer(Computer):
    def set_software(self, s):
        print('台式电脑安装软件:', s.name)
        self.soft_list.append(s)

# 笔记本电脑
class LaptopComputer(Computer):
    def set_software(self, s):
        print('笔记本电脑安装软件:', s.name)
        self.soft_list.append(s)









