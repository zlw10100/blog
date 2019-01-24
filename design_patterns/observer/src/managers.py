# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""管理者模块
此模块连接发布者和订阅者模块，作为一个调度中心。
"""


class BaseManager(object):
    # 订阅映射表
    subscriber_map = dict()

    # 订阅
    def subscribe(self, subject, subscriber):
        raise NotImplementedError

    # 退订
    def unsubscribe(self, subject, subscriber):
        raise NotImplementedError

    # 发布
    def publish(self, subject, *args, **kwargs):
        raise NotImplementedError


class VueManager(BaseManager):
    # 订阅
    def subscribe(self, subject, subscriber):
        if subject not in self.subscriber_map:
            self.subscriber_map[subject] = list()
        self.subscriber_map[subject].append(subscriber)

    # 退订
    def unsubscribe(self, subject, subscriber):
        self.subscriber_map.get(subject).remove(subscriber)

    # 发布
    def publish(self, subject, *args, **kwargs):
        for subscriber in self.subscriber_map.get(subject):
            subscriber.callback(*args, **kwargs)
