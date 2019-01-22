# -*- coding: utf-8 -*-
# 'author':'zlw'


from basic_linked_list import SingleLinkedList, Element


class CycleElement(Element):
    def __init__(self, value):
        super().__init__(value)
        self.prev_element = None

# 双向链表
class DoubleLinkedList(SingleLinkedList):
    element_class = CycleElement

    def __init__(self, init_values=None):
        # 创建链表
        super().__init__(init_values)

    @property
    def values_left(self):
        # 反向返回数据列表
        return list(reversed(self.values))

    def _confirm_element(self, target_element):
        """元素确认函数"""
        super()._confirm_element(target_element)

        # 元素应该是一个单元素，不应该是另一个链表的元素
        if target_element.prev_element is not None:
            raise ValueError(f'元素{target_element}不应该是其他链表的元素')

    def insert(self, position, target_element):
        """元素插入函数

        将元素插入到链表指定索引位置。
        插入的位置有2种情况：
            1. 插入到头结点
            2. 插入到中间节点或尾节点
        因为头节点设置了指针引用，所以要特殊处理，插入到尾节点并不影响指针引用可当做普通节点处理。

        如果插入时链表为空，则插入行为等价于追加一个元素。
        如果插入的索引位置是合法无效的(大于当前链表的长度)，则插入行为等价于追加一个元素。
        如果插入的索引位置是不合法的(索引值小于0)，则抛出索引值异常。
        """

        self._confirm_element(target_element)

        if position < 0:  # 非法索引值
            raise KeyError('索引值不能为负数')

        if self.is_empty or position >= self.length:  # 等价于追加操作
            return self.append(target_element)

        tobe_insert_element = self.select(position)  # 待插入元素
        if tobe_insert_element is self.head:
            return self.append_left(target_element)
        else:  # 普通情况
            prev_element = self.select(position - 1)
            prev_element.next_element = target_element
            target_element.next_element = tobe_insert_element

    def append(self, target_element):
        """元素追加函数

        特别注意，因为尾节点设置了指针引用，所以需要特殊处理引用变更。
        """

        self._confirm_element(target_element)

        # 处理空表
        if self.is_empty:
            self.head = self.tail = target_element
        else:
            # 向末尾追加一个元素
            self.tail.next_element = target_element
            self.tail = target_element

    def append_left(self, target_element):
        """元素左追加函数

        此函数直接追加到头结点位置，需要特别注意修改头节点指针引用。
        """

        self._confirm_element(target_element)

        # 处理空表
        if self.is_empty:
            self.head = self.tail = target_element
        else:
            # 向头结点追加一个元素
            target_element.next_element = self.head
            self.head = target_element

    def update(self, position, target_element):
        """元素更新函数
        根据给定的位置和给定的元素更新链表
        要特别注意更新头尾节点的特殊情况。
        """

        self._confirm_element(target_element)

        tobe_update_element = self.select(position)
        if not tobe_update_element:
            raise KeyError(f'未找到位置为{position}的元素')

        # 替换指定位置的元素
        if tobe_update_element is self.head:
            target_element.next_element = self.head.next_element
            self.head = target_element
        else:
            prev_element = self.select(position - 1)
            if tobe_update_element is self.tail:
                prev_element.next_element = target_element
                self.tail = target_element
            else:
                prev_element.next_element = target_element
                target_element.next_element = tobe_update_element.next_element

    def pop(self, position=None):
        # 删除指定位置的元素
        if self.is_empty:
            raise KeyError(f'当前链表已经为空，无法弹出元素')

        # 判断索引位置的合法性
        if position is None:
            position = self.length - 1
        else:
            if position < 0 or position >= self.length:
                raise KeyError('索引值不合法')

        # 合法的索引值
        tobe_pop_element = self.select(position)
        if tobe_pop_element is self.head:
            self.head = self.head.next_element
        else:
            prev_element = self.select(position - 1)
            if tobe_pop_element is self.tail:
                prev_element.next_element = self.tail.next_element
                self.tail = prev_element
            else:
                prev_element.next_element = tobe_pop_element.next_element

        tobe_pop_element.next_element = None
        return tobe_pop_element
