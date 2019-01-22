# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
栈是一种操作被约束的线性表，可以使用数组或者链表来实现。
栈的操作特点是只在一端插入和删除元素。
栈的应用适合满足如下2个条件的业务场景：
    1. 需要保存历史状态以便后续访问
    2. 访问/操作顺序有特定要求，以正序和逆序的顺序访问数据
"""


class Element(object):
    def __init__(self, value):
        self.value = value
        self.next_element = None

    def __repr__(self):
        return f'ele({self.value})'

    __str__ = __repr__


# 使用链表来实现栈
class BasicStack(object):
    element_class = Element

    def __init__(self, max_size=None):
        self.top = None
        self.max_size = max_size
        self.cur_size = 0

    def __repr__(self):
        return f'{self.__class__.__name__}(max_size={self.max_size})'

    def __str__(self):
        elements_string = ''
        for element in self._traverse_each():
            temp_string = str(element) + ', '
            elements_string += temp_string
        return f'{self.__class__.__name__}: {elements_string}'

    def _each(self):
        yield 'ok'
        cur = self.top
        while cur:
            yield cur
            cur = cur.next_element

    def _traverse_each(self):
        if self.is_empty:
            return []
        else:
            each = self._each()
            each.send(None)
            return each
    
    @property
    def length(self):
        return self.cur_size

    # 栈的清空
    def clear(self):
        self.top = None
        self.cur_size = 0

    # 栈是否满
    @property
    def is_full(self):
        if self.max_size is None:
            return False
        return self.cur_size >= self.max_size

    # 栈是否空
    @property
    def is_empty(self):
        return self.top is None

    # 入栈操作
    def push(self, target_value):
        # 判断栈是否已满，如果已满则抛出异常
        if self.is_full:
            raise RuntimeError(f'栈{self}已满，目标值<{target_value}>无法入栈')

        # 如果栈未满，则把目标元素值加入栈顶
        target_element = self.element_class(target_value)
        target_element.next_element = self.top
        self.top = target_element
        # 当前栈大小增加1
        self.cur_size += 1

    # 出栈操作
    def pop(self):
        # 判断栈是否已空，如果已空则抛出异常
        if self.is_empty:
            raise RuntimeError(f'栈{self}已空，无法弹出')

        # 如果未空，则弹出栈顶元素值
        target_element = self.top
        self.top = self.top.next_element
        # 当前栈大小减少1
        self.cur_size -= 1

        target_element.next_element = None
        return target_element.value
