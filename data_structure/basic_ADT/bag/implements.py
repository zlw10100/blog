# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
# 第三步，编写实现
抽象数据结构: 背包的实现模块。
有两种实现，一种基于数组，一种基于链表。
"""


from abc import ABCMeta, abstractmethod


class IteratorInterface(object):
    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class AbstractBag(IteratorInterface, metaclass=ABCMeta):
    """抽象背包类接口"""

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass


class BagArrayImplemented(AbstractBag):
    """基于数组实现的背包类"""

    init_size = 5

    def __init__(self):
        # 定义底层实现
        self.max_size = self.init_size
        self.array = [None] * self.max_size
        self.cur_index = 0
        self.cur_size = 0
        self.iter_index = None

    def add(self, item):
        # 动态容量扩展
        if (self.cur_size + 1) >= (self.max_size // 2):
            self._resize(self.max_size * 2)

        self.array[self.cur_index] = item
        self.cur_index += 1
        self.cur_size += 1

    def is_empty(self):
        return self.cur_size == 0

    def size(self):
        return self.cur_size

    def __iter__(self):
        if self.cur_size != 0:
            self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index is None:
            raise StopIteration

        elif self.iter_index >= self.cur_size:
            raise StopIteration

        else:
            item = self.array[self.iter_index]
            self.iter_index += 1
            return item

    def _resize(self, new_size):
        assert new_size > self.cur_size, f'动态调整容量时发生逻辑错误'

        new_array = [None] * new_size
        for i in range(self.cur_size):
            new_array[i] = self.array[i]

        self.array = new_array
        self.max_size = new_size


class BagLinkedListImplemented(AbstractBag):
    """基于链表实现的背包类"""

    def __init__(self):
        # 定义底层实现
        self.head = None
        self.cur_size = 0
        self.iter_pointer = None

    def add(self, item):
        self.old_head = self.head
        self.head = self.Node(item)
        self.head.next_node = self.old_head
        self.cur_size += 1

    def is_empty(self):
        return self.cur_size == 0

    def size(self):
        return self.cur_size

    def __iter__(self):
        if self.cur_size != 0:
            self.iter_pointer = self.head
        return self

    def __next__(self):
        if self.iter_pointer is None:
            raise StopIteration
        else:
            item = self.iter_pointer.item
            self.iter_pointer = self.iter_pointer.next_node
            return item

    class Node(object):  # 私有嵌套类
        def __init__(self, item=None):
            self.item = item
            self.next_node = None


# 控制对外提供的实现
DefaultBag = BagLinkedListImplemented
