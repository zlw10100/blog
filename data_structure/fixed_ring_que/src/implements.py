# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/2/1


"""固长环形队列实现"""


from .api import (
    AbstractFixedRingQue,
    QueIsEmptyError,
    QueIsFullError,
)


class ArrayImplementation(AbstractFixedRingQue):
    """数组实现"""

    def __init__(self, max_size):
        # 初始化底层实现
        self.max_size = max_size
        self.array = [None] * self.max_size
        self.head_index = None
        self.tail_index = None
        self.cur_size = 0
        self.iter_index = None
        self.iter_size = 0

    def enqueue(self, item):
        if self.is_full():
            raise QueIsFullError
        else:
            self._enqueue(item)

    def _enqueue(self, item):
        assert not self.is_full(), f'队列已满无法入队'

        self._extend_tail()
        self.array[self.tail_index] = item
        self.cur_size += 1

    def _extend_tail(self):
        if self.is_empty():  # 特殊处理从空->单元素的情况
            self.head_index = self.tail_index = 0
        else:
            self.tail_index += 1
            if self.tail_index == self.max_size:
                self.tail_index = 0

    def dequeue(self):
        if self.is_empty():
            raise QueIsEmptyError
        else:
            item = self._dequeue()
            return item

    def _dequeue(self):
        assert not self.is_empty(), f'队列已空无法出队'

        item = self.array[self.head_index]
        self.array[self.head_index] = None
        self.cur_size -= 1

        self._shorten_head()
        return item

    def _shorten_head(self):
        if self.head_index is self.tail_index:  # 特殊处理单元素->空的情况
            self.head_index = self.tail_index = None
        else:
            self.head_index += 1
            if self.head_index == self.max_size:
                self.head_index = 0

    def is_empty(self):
        return (
            self.head_index is self.tail_index and
            self.tail_index is None
        )

    def is_full(self):
        return self.cur_size == self.max_size

    def size(self):
        return self.cur_size

    def __iter__(self):
        self._check_iter()
        return self

    def _check_iter(self):
        if self.is_empty():
            return None
        else:
            self.iter_index = self.head_index
            self.iter_size = 0
            return None

    def __next__(self):
        if self.iter_index is None:
            raise StopIteration
        elif self.iter_size == self.cur_size:
            self._clear_iter()
            raise StopIteration
        else:
            item = self.array[self.iter_index]
            self._update_iter()
            return item

    def _clear_iter(self):
        self.iter_index = None
        self.iter_size = 0

    def _update_iter(self):
        self.iter_size += 1
        self.iter_index += 1

        if self.iter_index != self.max_size:
            return None
        else:
            self.iter_index = 0
            return None


class LinkedListImplementation(AbstractFixedRingQue):
    """链表实现"""

    def __init__(self, max_size):
        # 初始化底层实现
        self.max_size = max_size
        self.head = None
        self.tail = None
        self.cur_size = 0
        self.iter_pointer = None

    def enqueue(self, item):
        if self.is_full():
            raise QueIsFullError
        else:
            self._enqueue(item)

    def _enqueue(self, item):
        assert not self.is_full(), f'队列已满无法入队'

        new_node = self.Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            old_tail = self.tail
            self.tail = new_node
            old_tail.next_node = self.tail

        self.cur_size += 1

    def dequeue(self):
        if self.is_empty():
            raise QueIsEmptyError
        else:
            item = self._dequeue()
            return item

    def _dequeue(self):
        assert not self.is_empty(), f'队列已空无法出队'

        item = self.head.item
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next_node

        self.cur_size -= 1
        return item

    def is_empty(self):
        return (
            self.head is self.tail and
            self.tail is None
        )

    def is_full(self):
        return self.cur_size == self.max_size

    def size(self):
        return self.cur_size

    def __iter__(self):
        self._check_iter()
        return self

    def _check_iter(self):
        if self.is_empty():
            return None
        else:
            self.iter_pointer = self.head
            return None

    def __next__(self):
        if self.iter_pointer is None:
            raise StopIteration
        else:
            item = self.iter_pointer.item
            self.iter_pointer = self.iter_pointer.next_node
            return item

    class Node(object):
        def __init__(self, item):
            self.item = item
            self.next_node = None


RingQue = ArrayImplementation
