# !/usr/bin/python
# -*- coding:utf-8 -*-


# 第一步，定义api
"""
队列api定义：
一个支持先进先出的集合。

class Queue<Item>:
    Queue()                     实例化一个队列对象

    void enqueue(Item item)     将元素入队
    Item dequeue()              出队元素
    bool is_empty()             队列判空
    int size()                  返回队列当前容量
    __iter__                    返回队列迭代器对象
    __next__                    返回迭代器中下一个元素
"""


from abc import ABCMeta, abstractmethod


class IteratorInterface(object):
    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class AbstractQueue(IteratorInterface):
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
    def size(self):
        pass


class Error(Exception):
    pass


class QueueIsEmptyError(Error):
    pass


