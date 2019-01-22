# -*- coding: utf-8 -*-
# 'author':'zlw'



# 设置链表的节点
class ListNode(object):
    def __init__(self, value):
        # 节点的数据域的值
        self.value = value
        # 线性表的前置节点引用
        self.prev_node = None
        # 线性表的后置节点引用
        self.next_node = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        string = f'node({self.value})'
        return string


class DoubleCycleLinkedList(object):
    # 双向循环链表
    node_class = ListNode

    # 实例对象初始化
    def __init__(self, values=None):
        self.init_values = values
        self.head = None
        self.tail = None

        # 启动链表创建
        self._create()

    # 管理接口 =========================
    def _create(self):
        """链表创建函数

        内部接口，判定用户是否给定链表的值序列，如果有，则创建链表，否则什么也不做。
        函数没有返回值。
        """

        # 如果用户没有给定任何初始值，则创建一个空链表
        if self.init_values is None:
            return None
        else:
            # 如果用户给定了初始的值序列则创建链表
            nodes = [self.node_class(value) for value in self.init_values]
            for node in nodes:
                self.append(node)
            return None

    def _each(self):
        """链表节点遍历生成器 """

        # 该接口要求调用的链表不能为空
        assert not self.is_empty, '内部遍历接口要求链表不能为空'

        yield 'ok'
        yield self.head

        current_node = self.head.next_node
        while current_node != self.head:
            yield current_node
            current_node = current_node.next_node

    def traverse_each(self):
        """遍历函数
        内部接口，遍历当前链表并逐个节点返回
        """

        if self.is_empty:
            each = list()
        else:
            each = self._each()
            each.send(None)
        return each

    @property
    def is_empty(self):
        return self.head is self.head is None

    @property
    def length(self):
        """获取链表的长度

        因为用户可以自行通过自己的实现直接对节点操作，所以保存链表的长度为属性值是不准确的。
        每一次调用长度获取时都应该遍历当前的链表以确定准确的长度。
        """

        if self.is_empty:
            return 0
        else:
            count = 0
            for node in self.traverse_each():
                count += 1
            return count

    @property
    def values(self):
        v_list = list()
        if not self.is_empty:
            for node in self.traverse_each():
                v_list.append(node.value)
        return v_list

    @property
    def values_left(self):
        values = self.values
        values.reverse()
        return values

    def __repr__(self):
        format_repr = f'Empty DoubleCycle-Linked-List in <{id(self)}> with {type(self)}'
        if not self.is_empty:
            format_repr = f'{self.__class__.__name__}({[repr(node) for node in self.traverse_each()]})'
        return format_repr

    def __str__(self):
        format_string = 'Empty DoubleCycle-Linked-List'

        if not self.is_empty:
            format_string = 'DoubleCycle-Linked-List: '

            nodes_string = list()
            for node in self.traverse_each():
                nodes_string.append(str(node))

            link_string = ''
            for i, node_string in enumerate(nodes_string):
                link_string += f'<{i}>{node_string}, '

            format_string += link_string
        return format_string

    # 查询接口===========================

    def locate(self, target_node):
        """节点搜索函数
        根据给定的节点搜索链表中所在的位置
        """

        index = -1
        if not self.is_empty:
            for i, node in enumerate(self.traverse_each()):
                if node is target_node:
                    index = i
                    break
        return index

    def select(self, position):
        """节点选择函数
        根据给定的位置返回链表中的节点
        """

        target_node = None
        if not self.is_empty:
            for i, node in enumerate(self.traverse_each()):
                if i == position:
                    target_node = node
                    break
        return target_node

    # 修改接口==============================

    def insert(self, position, target_node):
        """节点插入接口

        为了和内置的python列表插入接口保持一致，当链表为空的时候就等价于追加节点
        当插入的位置不存在时，也等价于追加
        插入节点要考虑插入收尾节点的特殊情况
        """

        if position < 0:
            raise KeyError('插入索引位置不能为负')

        # 如果链表为空或者目标位置大于最大索引值，则插入操作等价于追加操作
        max_length = self.length
        if self.is_empty or position >= max_length:
            return self.append(target_node)
        else:
            # 否则，考虑插入收尾节点的特殊情况
            if position == 0:
                # 插入头部
                return self.append_left(target_node)
            elif position == max_length - 1:
                # 插入尾部
                return self.append(target_node)
            else:
                # 考虑普通情况
                inserted_node = self.select(position)
                # 向右
                inserted_node.prev_node.next_node = target_node
                target_node.next_node = inserted_node
                # 向左
                inserted_node.prev_node = target_node
                target_node.prev_node = inserted_node.prev_node

    def update(self, position, target_node):
        """节点更新函数
        根据给定的节点更新指定位置的节点
        要特别注意如果指定位置是head或者tail需要更新两个头尾指针引用
        """

        # 空链表无法更新，抛出异常
        if self.is_empty:
            raise RuntimeError(f'更新失败，链表为空：{repr(self)}')

        # 判断位置的合法性
        old_node = self.select(position)
        if not old_node:
            raise KeyError(f'未找到位置{position}处的节点')

        # 处理只有一个节点时的特殊情况
        if self.length == 1:
            self.head = self.tail = target_node
            target_node.next_node = self.head
            target_node.prev_node = self.head
        # 处理更新位置是头尾节点的特殊情况
        elif old_node is self.head:
            # 向右
            target_node.next_node = self.head.next_node
            self.tail.next_node = target_node

            # 向左
            self.head.next_node.prev_node = target_node
            target_node.prev_node = self.tail

            # 更新头结点
            self.head = target_node
        elif old_node is self.tail:
            # 向右
            self.tail.prev_node.next_node = target_node
            target_node.next_node = self.head

            # 向左
            self.head.prev_node = target_node
            target_node.prev_node = self.tail.prev_node

            # 更新尾节点
            self.tail = target_node
        else:
            # 处理普通情况
            # 向右
            old_node.prev_node.next_node = target_node
            target_node.next_node = old_node.next_node

            # 向左
            old_node.next_node.prev_node = target_node
            target_node.prev_node = old_node.prev_node

    def delete(self, target_node):
        # 移除指定的节点并返回,此接口默认目标节点存在于链表中

        # 如果链表是空的，则抛出异常
        if self.is_empty:
            raise RuntimeError(f'链表为空，无法删除: {self}')

        # 如果只有一个节点的特殊情况
        if self.length == 1:
            self.head = self.tail = None
        # 否则
        else:
            # 如果是头结点
            if target_node is self.head:
                self.head = target_node.next_node
                self.tail.next_node = self.head
                self.head.prev_node = self.tail
            # 如果是尾节点
            elif target_node is self.tail:
                self.tail = target_node.prev_node
                self.tail.next_node = self.head
                self.head.prev_node = self.tail
            # 普通情况
            else:
                target_node.prev_node.next_node = target_node.next_node
                target_node.next_node.prev_node = target_node.prev_node

        # 返回被删除的节点
        target_node.next_node = None
        target_node.prev_node = None
        return target_node

    def pop(self, position=None):
        """节点删除函数

        特别注意如果删除的是收尾节点的特殊情况
        """

        # 如果链表是空的，则抛出异常
        if self.is_empty:
            raise RuntimeError(f'链表为空，无法删除: {self}')

        # 判断位置合法性
        tobe_deleted_node = self.select(position) if position is not None else self.tail
        if not tobe_deleted_node:
            raise KeyError(f'链表未找到位置为{position}的节点')

        # 否则如果只有一个节点的特殊情况
        if self.length == 1:
            self.head = self.tail = None
        # 否则
        else:
            # 如果是头结点
            if tobe_deleted_node is self.head:
                self.head = tobe_deleted_node.next_node
                self.tail.next_node = self.head
                self.head.prev_node = self.tail
            # 如果是尾节点
            elif tobe_deleted_node is self.tail:
                self.tail = tobe_deleted_node.prev_node
                self.tail.next_node = self.head
                self.head.prev_node = self.tail
            # 普通情况
            else:
                tobe_deleted_node.prev_node.next_node = tobe_deleted_node.next_node
                tobe_deleted_node.next_node.prev_node = tobe_deleted_node.prev_node

        # 返回被删除的节点
        tobe_deleted_node.next_node = None
        tobe_deleted_node.prev_node = None
        return tobe_deleted_node

    def append(self, target_node):
        """追加节点
        追加节点到链表的最右侧
        """

        # 判定节点合法性
        self._confirm(target_node)

        # 如果当前是空表，说明追加的是第一个节点
        if self.is_empty:
            self.head = self.tail = target_node
            target_node.next_node = self.head
            target_node.prev_node = self.head
        else:
            # 否则，追加的节点作为最右的节点（尾节点）
            self.tail.next_node = target_node
            target_node.next_node = self.head

            self.head.prev_node = target_node
            target_node.prev_node = self.tail

            # 更新尾节点
            self.tail = target_node

    def append_left(self, target_node):
        """在头部追加节点
        在链表的头部追加节点
        """

        # 判断待增加节点的合法性
        self._confirm(target_node)

        # 处理如果当前链表为空的特殊情况
        if self.is_empty:
            self.head = self.tail = target_node
            target_node.next_node = self.head
            target_node.prev_node = self.head
        else:
            # 向右侧
            self.tail.next_node = target_node
            target_node.next_node = self.head

            # 向左侧
            self.head.prev_node = target_node
            target_node.prev_node = self.tail

            # 更新头结点
            self.head = target_node

    def _confirm(self, target_node):
        """节点判断函数

        判断节点如果是单独节点，这是正常的情况。
        判断节点如果属于另一个链表，则抛出错误不允许增加
        """

        # 判断节点类型
        if not isinstance(target_node, self.node_class):
            raise TypeError(f'追加的节点类型错误,期望类型:{self.node_class.__name__}')

        # 判断追加的是单节点还是另一个链表
        if (target_node.next_node is not None) or (target_node.prev_node is not None):
            raise ValueError('你追加的不是单独节点')


if __name__ == '__main__':
    mylist = DoubleCycleLinkedList()
    mylist.append(ListNode(23))
    mylist.append(ListNode(93))
    print(mylist.values)
