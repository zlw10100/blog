# !/usr/bin/python
# -*- coding:utf-8 -*-


"""
栈的实现模块
基于数组以及链表。
"""


from abc import ABCMeta, abstractmethod


class Error(Exception):
    pass


class StackIsEmptyError(Error):
    pass


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


class StackArrayImplemented(AbstractStack):
    """基于数组的栈实现"""

    init_size = 5

    def __init__(self):
        # 初始化底层实现
        self.max_size = self.init_size
        self.array = [None] * self.max_size
        self.top = None
        self.cur_size = 0
        self.iter_index = None

    def push(self, item):
        if self.top is None:
            self.top = 0
        else:
            self.top += 1

        self.array[self.top] = item
        self.cur_size += 1

        # 容量检查
        self._check_resize()

    def pop(self):
        if self.is_empty():
            raise StackIsEmptyError()

        item = self.array[self.top]
        if self.top == 0:
            self.top = None
        else:
            self.top -= 1

        self.cur_size -= 1
        # 容量检查
        self._check_resize()

        return item

    def is_empty(self):
        return self.cur_size == 0

    def size(self):
        return self.cur_size

    def _check_resize(self):
        if self.cur_size >= (self.max_size // 2):
            new_size = self.max_size * 2
        elif self.cur_size < (self.max_size // 4):
            new_size = self.max_size // 2
        else:
            return None

        # 执行空间调整
        new_array = [None] * new_size
        for i in range(self.cur_size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.max_size = new_size

    def __iter__(self):
        if self.cur_size != 0:
            self.iter_index = self.cur_size - 1
        return self

    def __next__(self):
        if self.iter_index is None:
            raise StopIteration

        if self.iter_index < 0:
            raise StopIteration

        item = self.array[self.iter_index]
        self.iter_index -= 1
        return item


class StackLinkedListImplemented(AbstractStack):
    """基于链表的栈实现"""

    def __init__(self):
        # 初始化底层实现
        self.head = None
        self.cur_size = 0
        self.iter_pointer = None

    def push(self, item):
        new_node = self.Node(item)
        old_head = self.head
        self.head = new_node
        self.head.next_node = old_head
        self.cur_size += 1

    def pop(self):
        if self.is_empty():
            raise StackIsEmptyError

        item = self.head.item
        self.head = self.head.next_node
        self.cur_size -= 1
        return item

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

        item = self.iter_pointer.item
        self.iter_pointer = self.iter_pointer.next_node
        return item

    class Node(object):  # 私有嵌套类
        def __init__(self, item=None):
            self.item = item
            self.next_node = None


DefaultStack = StackLinkedListImplemented
