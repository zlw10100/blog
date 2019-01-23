# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""建造者模块
为每一个业务类一对一的映射一个建造者类，此类中详细定义了此业务类的构造细节。
"""

from abc import ABCMeta, abstractmethod

from src.products import Museum, Opera


# 建造者基类,所有业务类的构造过程均在此定义
class BaseBuilder(object, metaclass=ABCMeta):
    @abstractmethod  # 建造基座
    def build_base(self):pass

    @abstractmethod  # 建造墙面
    def build_wall(self):pass

    @abstractmethod  # 获取最终产品对象
    def get_result(self):pass


class MuseumBuilder(BaseBuilder):
    def __init__(self):
        self.museum = Museum()  # 每一个建造者对象负责一个业务类对象
    
    # 由此类负责对应产品的固定构造
    def build_base(self):
        self.museum.add('博物馆的基座')

    def build_wall(self):
        self.museum.add('博物馆的墙面')
    
    def get_result(self):
        return self.museum
    

class OperaBuilder(BaseBuilder):
    def __init__(self):
        self.opera = Opera()  # 每一个建造者对象负责一个业务类对象

    # 由此类负责对应产品的固定构造
    def build_base(self):
        self.opera.add('歌剧院的基座')

    def build_wall(self):
        self.opera.add('歌剧院的墙面')

    def get_result(self):
        return self.opera
