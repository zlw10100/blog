# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/29


from src.base import (
    AbstractQueue,
    QueueIsFullError,
    QueueIsEmptyError,
)


class RQueueArrayImplemented(AbstractQueue):
    """基于数组的可变长队列实现"""

    init_size = 5

    def __init__(self, fixed_size=None):
        super().__init__(fixed_size)

        # 初始化底层实现
        self.max_size = self.fixed_size or self.init_size
        self.array = [None] * self.max_size
        self.head_index = None
        self.tail_index = None
        self.cur_size = 0
        self.iter_index = None
        self.iter_size = 0

    def enqueue(self, item):
        """入队实现

        0. 判断队列是否已满
        1. 判定队列是否已空并增加队尾索引
        2. 判断队尾索引是否越界(固定容量时)
        3. 在队尾处增加元素
        4. 增加队列有效容量
        5. 根据当前有效容量检查并调整数组大小
        """

        if self.is_full():
            raise QueueIsFullError()

        if self.is_empty():
            self.head_index = self.tail_index = 0
        else:
            self.tail_index += 1
            if self.tail_index == self.fixed_size:
                self.tail_index = 0  # 越界时跳回到数组首位

        self.array[self.tail_index] = item
        self.cur_size += 1

        self._check_resize()

    def dequeue(self):
        """出队实现

        0. 判断队列是否已空
        1. 判断队列是否单元素
        2. 获取队头元素
        3. 增加队头索引
        4. 判断队头索引是否越界(固定容量时)
        5. 减小队列有效容量
        6. 根据当前有效容量检查并调整数组大小
        """

        if self.is_empty():
            raise QueueIsEmptyError()

        item = self.array[self.head_index]
        if self.head_index is self.tail_index:
            self.head_index = self.tail_index = None
        else:
            self.head_index += 1
            if self.head_index == self.fixed_size:
                self.head_index = 0  # 处理越界

        self.cur_size -= 1
        self._check_resize()

        return item

    def is_empty(self):
        return (
            self.head_index is self.tail_index
            and self.head_index is None
        )

    def is_full(self):
        if (
            self.fixed_size is not None
            and self.cur_size ==  self.fixed_size
        ):
            return True
        return False

    def size(self):
        return self.cur_size

    def __iter__(self):
        if not self.is_empty():
            self.iter_index = self.head_index
            self.iter_size = 0
        return self

    def __next__(self):
        if self.iter_index is None:
            raise StopIteration

        if self.iter_size == self.cur_size:
            raise StopIteration

        item = self.array[self.iter_index]
        self.iter_index += 1
        if self.iter_index == self.fixed_size:
            self.iter_index = 0  # 处理固定容量时越界问题
        self.iter_size += 1

        return item

    def _check_resize(self):
        if self.is_empty():
            return None

        if self.fixed_size is not None:
            return None

        if self.cur_size >= (self.max_size // 2):
            new_size = self.max_size * 2
        elif 0 < self.cur_size < (self.max_size // 4):
            new_size = self.max_size // 2
        else:
            return None

        new_array = [None] * new_size
        for index, item in enumerate(self):
            new_array[index] = item

        self.array = new_array
        self.max_size = new_size
        self.head_index = 0
        self.tail_index = self.cur_size - 1


class RQueueLinkedListImplemented(AbstractQueue):
    """基于链表的可变长队列实现"""

    def __init__(self, fixed_size=None):
        super().__init__(fixed_size)

        # 初始化底层实现
        self.head = None
        self.tail = None
        self.cur_size = 0
        self.iter_pointer = None

    def enqueue(self, item):
        if self.is_full():
            raise QueueIsFullError()

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
            raise QueueIsEmptyError()

        item = self.head.item
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next_node

        self.cur_size -= 1
        return item

    def is_empty(self):
        return (
            self.head is self.tail
            and self.tail is None
        )

    def is_full(self):
        if (
            self.fixed_size is not None
            and self.cur_size == self.fixed_size
        ):
            return True
        return False

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

    class Node(object):
        def __init__(self, item=None):
            self.item = item
            self.next_node = None


# 对外统一接口
RQueue = RQueueLinkedListImplemented
