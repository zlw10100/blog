# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/29


from abc import ABCMeta, abstractmethod


# 定义迭代器接口
class IteratorInterface(object):
    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


# 定义错误类
class Error(Exception):
    pass


class QueueIsEmptyError(Error):
    pass


class QueueIsFullError(Error):
    pass


# 定义队列接口
class AbstractQueue(IteratorInterface, metaclass=ABCMeta):
    def __init__(self, fixed_size=None):
        self.fixed_size = fixed_size

    @abstractmethod
    def enqueue(self, item):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_full(self):
        pass

    @abstractmethod
    def size(self):
        pass
