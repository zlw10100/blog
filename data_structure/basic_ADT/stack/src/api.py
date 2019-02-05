# !/usr/bin/python
# -*- coding:utf-8 -*-


# 定义api
"""
栈的定义：
一个后进先出的集合。

class Stack<Item>:
    Stack()                 实例化栈对象

    void push(Item item)    将元素入栈
    Item pop()              弹出栈顶元素
    bool is_empty()         判断栈是否为空
    int size()              返回栈的当前容量
    __iter__                返回栈的迭代器对象
    __next__                返回迭代器中下一个元素
"""


from abc import ABCMeta, abstractmethod


class IteratorInterface(object):
    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class AbstractStack(IteratorInterface, metaclass=ABCMeta):
    @abstractmethod
    def push(self, item):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass


class Error(Exception):
    pass


class StackIsEmptyError(Error):
    pass
