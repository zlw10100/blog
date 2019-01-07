# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from src.products import Museum, Opera

from abc import ABCMeta, abstractmethod
# 建造者基类(建筑行业)
class BaseBuilder(object, metaclass=ABCMeta):
    # 要求所有产品固定的构造
    @abstractmethod  # 建造基座
    def build_base(self):pass

    @abstractmethod  # 建造墙面
    def build_wall(self):pass

    @abstractmethod  # 获取最终产品对象
    def get_result(self):pass

class MuseumBuilder(BaseBuilder):
    def __init__(self):
        self.museum = Museum()
    
    # 由此类负责对应产品的固定构造
    def build_base(self):
        self.museum.add('博物馆的基座')

    def build_wall(self):
        self.museum.add('博物馆的墙面')
    
    def get_result(self):
        return self.museum

# 同上，省略
class OperaBuilder(BaseBuilder): pass




