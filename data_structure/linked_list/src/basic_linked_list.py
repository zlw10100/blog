# -*- coding: utf-8 -*-
# 'author':'zlw'


class Element(object):
    """元素类
    用于链表元素，存储数据域和指针域
    """

    def __init__(self, value):
        self.value = value
        self.next_element = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return f'element({self.value})'


class SingleLinkedList(object):
    """单链表类
    单链表结构将一系列有序的链表元素串联在一起，单链表只有一个方向。
    """

    # 以组合方式设定链表元素类
    element_class = Element

    def __init__(self, init_values=None):
        # 链表初始化，设定头尾指针方便各类操作
        self.head = None
        self.tail = None
        self.init_values = init_values

        self.init_link()

    def __repr__(self):
        format_string = f'{self.__class__.__name__}({[repr(element) for element in self.traverse_each()]})'
        return format_string

    def __str__(self):
        format_string = 'Empty LinkedList'
        if not self.is_empty:
            format_string = 'LinkedList: '
            elements_string = ', '.join([f'<{i}>{str(element)}' for i, element in enumerate(self.traverse_each())])
            format_string += elements_string
        return format_string

    def init_link(self):
        if self.init_values:
            for value in self.init_values:
                element = self.element_class(value)
                self.append(element)

    @property
    def length(self):
        count = 0
        for element in self.traverse_each():
            count += 1
        return count

    @property
    def is_empty(self):
        # 判断是否表空
        return self.head is None

    @property
    def is_full(self):
        return False

    @property
    def values(self):
        # 返回链表元素的数据列表
        return [element.value for element in self.traverse_each()]

    def _each(self):
        """元素遍历底层api，生成器

        此函数在链表非空的情况下完成元素遍历，每次返回一个元素以供用于自定义处理。
        此函数未处理遍历结束后的StopIteration异常，调用者应该使用for处理遍历。
        """

        # 防御式编程，遍历要求链表必须非空
        assert not self.is_empty, '遍历生成器函数要求链表必须非空'

        yield 'ok'
        current_element = self.head
        while current_element is not None: # 单链表的尾节点指向None，所以是遍历终止条件
            yield current_element
            current_element = current_element.next_element

    def traverse_each(self):
        """逐元素遍历函数"""

        # 防御式编程，处理空表情况
        if self.is_empty:
            return list()
        else:
            # 非空条件下可以遍历
            each = self._each()
            # 初始化生成器
            each.send(None)
            return each

    def clear(self):
        # 清空链表
        self.head = self.tail = None

    def select(self, position):
        """元素选择函数

        根据给定的索引位置尝试获取链表中的元素。
        如果未找到该元素，则返回None。
        """

        target_element = None
        for i, element in enumerate(self.traverse_each()):
            if i == position:
                target_element = element
                break
        return target_element

    def locate(self, target_element):
        """元素定位函数

        根据给定的元素确定在链表中的索引位置。
        如果链表中未含有此元素，则返回-1。
        """

        # 找到指定元素的位置
        target_index = -1
        for i, element in enumerate(self.traverse_each()):
            if element is target_element:  # 元素定位判断应该使用is而不是==
                target_index = i
                break
        return target_index

    def _confirm_element(self, target_element):
        """元素确认函数

        此函数用于确认一个元素的合法性。
        元素不应该是另一个链表的元素，因为各类操作都会修改此元素的前后元素引用其他链表上断链的错误。
        """

        # 元素的类型应该归属于链表元素类型
        if not isinstance(target_element, self.element_class):
            raise TypeError(f'元素{target_element}的类型错误，期望类型:{self.element_class}')

        # 元素应该是一个单元素，不应该是另一个链表的元素
        if target_element.next_element is not None:
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
