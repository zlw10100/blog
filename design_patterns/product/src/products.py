# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


class Building(object):
    # 组件列表
    part_list = list()
    
    def add(self, part):
        # 增加部件
        self.part_list.append(part)

    def show(self):
        # 查看部件
        for part in self.part_list:
            print('部件:', part)


# 博物馆
class Museum(Building):
    pass

# 歌剧院
class Opera(Building):
    pass










