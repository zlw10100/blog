# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
委托模块
"""


# 事件委托类
class EventDelegate(object):
    event_map = dict()
    
    def register(self, subject, observer_callback):
        if subject not in self.event_map:
            self.event_map[subject] = [observer_callback]
        else:
            self.event_map[subject].append(observer_callback)


    def unregister(self):
        pass
    
    def update(self, subject):
        if subject in self.event_map:
            for observer_callback in self.event_map[subject]:
                # 调用观察者的回调函数
                observer_callback()
        










