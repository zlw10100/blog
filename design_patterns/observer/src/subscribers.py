# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""订阅者模块
此模块定义了订阅者的行为，订阅者将会根据收到的通知执行下一步操作。
"""


class BaseSubscriber(object):
    def callback(self, *args, **kwargs):
        raise NotImplementedError


class VueSubscriber(BaseSubscriber):
    def __init__(self):
        self.data = None

    def callback(self, new_data):
        self.data = new_data
        print('vue订阅者接收到更新的数据是:', new_data)
