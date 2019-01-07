# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod


class AbstractEvent(object, metaclass=ABCMeta):
    # 事件名称和对应的权级,还有额外的自定义字段
    def __init__(self, **extra):  
        for k, v in extra.items():
            setattr(self, k, v)

class SalaryIncreaseEvent(AbstractEvent):
    pass











