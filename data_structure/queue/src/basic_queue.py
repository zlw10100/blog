# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
队列是一种操作被约束的线性表，队列可以使用数组或者链表实现。
队列的约束操作是：
    在队列的一端追加元素，而在另一端弹出元素，满足FIFO的顺序特性。
"""


# 定义链表元素
class Element(object):
    def __init__(self, value):
        self.value = value
        self.next_element = None


# 基本的队列实现
class BasicQueue(object):
    element_class = Element

    # 实例对象初始化函数
    def __init__(self, max_size=None):
        # 提供队列最大值的设定
        self.max_size = max_size
        self.cur_size = 0
        # 头结点用于表示队列第一个元素，不被计算，当head和tail都指向头结点说明队列空
        self.first_element = self.element_class(None)
        self.head = self.first_element
        self.tail = self.first_element

    # 遍历队列生成器
    def _each(self):
        yield 'ok'
        cur = self.head.next_element
        while cur:
            yield cur
            cur = cur.next_element

    # 遍历队列公开api
    def traverse_each(self):
        if self.is_empty:
            return []
        else:
            each = self._each()
            next(each)  # 激活生成器
            return each

    # 清空队列
    def clear(self):
        self.head = self.tail = self.first_element
        self.cur_size = 0

    # 判定队列是否为满
    @property
    def is_full(self):
        if not self.max_size:
            return False
        else:
            return self.cur_size >= self.max_size

    # 判定队列是否为空
    @property
    def is_empty(self):
        return self.head is self.tail is self.first_element

    # 获取队列当前长度
    @property
    def length(self):
        return self.cur_size

    @property
    def values(self):
        # 获取队列的所有元素的值列表
        v_list = []
        for element in self.traverse_each():
            v_list.append(element.value)
        return v_list

        # 入队接口
    def put(self, value):
        """队列的入队接口函数

        该函数会将用户给定的值传入队列元素类并创建元素对象，然后尝试加入队列。
        """

        # 判断当前队列是否已经满了
        if self.is_full:
            # 如果满了则抛出异常
            raise RuntimeError(f'队列{self}已满，无法入队')
        else:
            # 如果没满，则实例化元素对象
            element = self.element_class(value)
            # 将实例化对象加入队列中，更新尾指针，更新队列长度
            self.tail.next_element = element
            self.tail = element
            self.cur_size += 1

    # 出队接口
    def get(self):
        """队列的出队接口函数

        在队列不为空的情况下，该函数将会弹出最新入队的元素
        """

        # 判断队列是否为空
        if self.is_empty:
            # 如果为空，则抛出异常
            raise RuntimeError(f'队列{self}已空,无法出队')
        else:
            # 否则，获得队头的元素，更新头指针，更新队列长度
            element = self.head.next_element
            self.head.next_element = element.next_element
            self.cur_size -= 1
            # 判断删除的元素是否是最后一个元素，如果是，则需要更新尾指针
            if element is self.tail:
                self.tail = self.head

            # 返回弹出的元素值
            element.next_element = None
            return element.value
