# -*- coding: utf-8 -*-
# 'author':'zlw'


"""单向循环链表只需要在单链表的api基础上增加尾节点对头结点的指向即可"""


from basic_linked_list import SingleLinkedList, Element


# 单向循环链表
class CycleLinkedList(SingleLinkedList):
    def __init__(self, init_values=None):
        # 创建链表
        super().__init__(init_values)

    def _each(self):
        """元素遍历底层api，生成器

        此函数在链表非空的情况下完成元素遍历，每次返回一个元素以供用于自定义处理。
        此函数未处理遍历结束后的StopIteration异常，调用者应该使用for处理遍历。
        """

        # 防御式编程，遍历要求链表必须非空
        assert not self.is_empty, '遍历生成器函数要求链表必须非空'

        yield 'ok'
        yield self.head

        current_element = self.head.next_element
        while current_element is not self.head: # 单循环链表的尾节点指向头结点，所以是遍历终止条件
            yield current_element
            current_element = current_element.next_element

    def append(self, target_element):
        """元素追加函数"""
        super().append(target_element)
        self.tail.next_element = self.head

    def append_left(self, target_element):
        """元素左追加函数"""
        super().append_left(target_element)
        self.tail.next_element = self.head

    def update(self, position, target_element):
        """元素更新函数"""
        super().update(position, target_element)
        self.tail.next_element = self.head

    def pop(self, position=None):
        p = super().pop(position)
        self.tail.next_element = self.head
        return p
