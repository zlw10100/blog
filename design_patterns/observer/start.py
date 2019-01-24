# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现观察者模式的程序
程序模拟vue的数据更新操作。
"""


from src.managers import VueManager
from src.publishers import VuePublisher
from src.subscribers import VueSubscriber


if __name__ == '__main__':
    # 实例化管理对象
    manager = VueManager()

    # 实例化发布者对象
    vue_publisher = VuePublisher(manager=manager)

    # 实例化订阅者对象
    vue = VueSubscriber()

    # 订阅
    manager.subscribe('vue_data_update', vue)
    print(manager.subscriber_map)
    # {'vue_data_update': [ < src.subscribers.VueSubscriber object at 0x00000210C690D0F0 >]}

    # 发布
    vue_publisher.publish('hello')
    # vue订阅者接收到更新的数据是: hello
    vue_publisher.publish('world')
    # vue订阅者接收到更新的数据是: world
