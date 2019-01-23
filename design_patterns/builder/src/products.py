# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""业务类(产品类)的定义模块"""


class BaseBuilding(object):  # 建筑物基类
    part_list = list()  # 组件列表
    
    def add(self, part):  # 增加部件
        self.part_list.append(part)

    def show(self):  # 查看部件
        for part in self.part_list:
            print('部件:', part)


# 博物馆
class Museum(BaseBuilding):
    pass

# 歌剧院
class Opera(BaseBuilding):
    pass
