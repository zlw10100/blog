# !/usr/bin/python
# -*- coding:utf-8 -*-


"""
队列实现模块
基于数组和链表分别实现队列接口。
"""


from abc import ABCMeta, abstractmethod


class Error(Exception):
    pass


class QueueIsEmptyError(Error):
    pass


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


class QueueArrayImplemented(AbstractQueue):
    """基于数组的队列实现

    因为队列需要两端均发生移动变化，所以以数组
    为存储实现的队列在出队元素后会浪费数组空间。
    解决方法：
        设定一个变量保存当前队列容量，根据当前
        容量和最大容量的比对，动态调整数组容量。
    """

    init_size = 5

    def __init__(self):
        # 定义底层实现
        self.max_size = self.init_size
        self.array = [None] * self.max_size
        self.cur_size = 0
        self.head_index = None
        self.tail_index = None
        self.iter_index = None

    def enqueue(self, item):
        if self.tail_index is None:
            self.tail_index = 0
            self.head_index = 0
        else:
            self.tail_index += 1

        self.array[self.tail_index] = item
        self.cur_size += 1

        # 容量检查
        self._check_resize()

    def dequeue(self):
        if self.is_empty():
            raise QueueIsEmptyError()

        item = self.array[self.head_index]
        self.head_index += 1
        if self.head_index > self.tail_index:
            self.head_index = self.tail_index = None
        self.cur_size -= 1

        # 容量检查
        self._check_resize()
        return item

    def is_empty(self):
        return self.head_index is self.tail_index is None

    def size(self):
        return self.cur_size

    def __iter__(self):
        if self.cur_size != 0:
            self.iter_index = self.head_index
        return self

    def __next__(self):
        if self.iter_index is None:
            raise StopIteration

        if self.iter_index > self.tail_index:
            raise StopIteration

        item = self.array[self.iter_index]
        self.iter_index += 1
        return item

    def _check_resize(self):
        if self.cur_size >= (self.max_size // 2):
            new_size = self.max_size * 2
        elif self.cur_size < (self.max_size // 4):
            new_size = self.max_size // 2
        else:
            return None

        # 调整数组大小
        new_array = [None] * new_size

        for index, item in enumerate(self):
            new_array[index] = item
        self.array = new_array
        self.max_size = new_size
        self.head_index = 0
        self.tail_index = self.cur_size - 1


class QueueLinkedListImplemented(AbstractQueue):
    """基于链表的队列实现"""

    def __init__(self):
        # 定义底层实现
        self.head = None
        self.tail = None
        self.cur_size = 0
        self.iter_pointer = None

    def enqueue(self, item):
        new_node = self.Node(item)

        if self.head is self.tail is None:  # 空链表
            self.head = self.tail = new_node
        else:
            old_tail = self.tail
            self.tail = new_node
            old_tail.next_node = self.tail

        self.cur_size += 1

    def dequeue(self):
        if self.is_empty():
            raise QueueIsEmptyError()

        item = self.head.item
        if self.head is self.tail:  # 单节点
            self.head = self.tail = None
        else:
            self.head = self.head.next_node

        self.cur_size -= 1
        return item

    def is_empty(self):
        return self.head is self.tail is None

    def size(self):
        return self.cur_size

    def __iter__(self):
        if not self.is_empty():
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


DefaultQueue = QueueLinkedListImplemented
