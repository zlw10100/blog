# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""发布者模块
此模块定义了发布者服务，发布者可以发布通知。
"""


class BasePublisher(object):
    subject = ''

    def __init__(self, manager):
        self.manager = manager

    def publish(self, *args, **kwargs):
        self.manager.publish(self.subject, *args, **kwargs)


class VuePublisher(BasePublisher):
    subject = 'vue_data_update'
