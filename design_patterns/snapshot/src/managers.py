# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""管理者模块
此模块负责管理快照过程。
"""


class AbstractManager(object):
    def save(self, index, snapshot):
        pass

    def extract(self, index):
        pass


class GameManager(AbstractManager):
    snapshot_map = dict()

    # 保存快照
    def save(self, index, snapshot):
        self.snapshot_map[index] = snapshot

    # 提取快照
    def extract(self, index):
        return self.snapshot_map.get(index)
