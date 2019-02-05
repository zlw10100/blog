# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
# 第三步，编写实现
抽象数据结构: 背包的实现模块。
有两种实现，一种基于数组，一种基于链表。
"""


from .api import AbstractBag


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
        self.array[self.cur_index] = item
        self.cur_index += 1
        self.cur_size += 1

        # 容量检查
        self._check_resize()

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

    def _check_resize(self):
        if self.cur_size >= (self.max_size // 2):
            new_size = self.max_size * 2
        else:
            return None

        # 执行容量调整
        new_array = [None] * new_size
        for i in range(self.cur_size):
            new_array[i] = self.array[i]

        self.array = new_array
        self.max_size = new_size

    def iter_item(self):
        if self.is_empty():
            return list()
        else:
            return self._iter_item()

    def _iter_item(self):
        item_list = list()
        cur_index = 0

        def is_stop():
            return True if cur_index == self.cur_size else False

        def handle():
            item_list.append(self.array[cur_index])

        def move_next():
            nonlocal cur_index
            cur_index += 1

        def recursion():
            if is_stop() is True:
                return None
            else:
                handle()
                move_next()
                return recursion()

        recursion()
        return item_list


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

    def iter_item(self):
        if self.is_empty():
            return list()
        else:
            return self._iter_item()

    def _iter_item(self):
        item_list = list()
        cur_node = self.head

        def is_stop():
            return True if cur_node is None else False

        def handle():
            item_list.append(cur_node.item)

        def move_next():
            nonlocal cur_node
            cur_node = cur_node.next_node

        def recursion():
            if is_stop() is True:
                return None
            else:
                handle()
                move_next()
                return recursion()

        recursion()
        return item_list

# 控制对外提供的实现
Bag = BagLinkedListImplemented
