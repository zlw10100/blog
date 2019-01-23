# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""电脑模块
此模块定义了各种电脑。
"""


from abc import ABCMeta, abstractmethod


class AbstractComputer(object, metaclass=ABCMeta):
    def __init__(self):
        self.software_list = list()
        
    @abstractmethod
    def set_software(self, soft_ware):
        pass

    def show_softwares(self):
        print(self.software_list)

# 台式电脑
class DesktopComputer(AbstractComputer):
    def set_software(self, soft_ware):
        print('台式电脑安装软件:', soft_ware.name)
        self.software_list.append(soft_ware)

# 笔记本电脑
class LaptopComputer(AbstractComputer):
    def set_software(self, soft_ware):
        print('笔记本电脑安装软件:', soft_ware.name)
        self.software_list.append(soft_ware)
