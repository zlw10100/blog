# -*- coding: utf-8 -*-
# 'author': 'zlw'


"""
两个队列模拟一个栈的实现。
以两个队列中最小容量的队列作为模拟栈的最大容量。
每次入栈数据，两个队列只有其中一个队列有数据，另一个队列为空，用于交换数据以实现FILO。
每次出栈数据，有数据的队列将前n-1个数据交换到另一个队列，然后当前队列出队。
每一次入栈的操作复杂度是O(1)，只需要在有数据的队列追加数据即可。
每一次出栈的操作副再度是O(n)，因为每次出栈前都需要交换前n-1个数据到另一个空队列中。

使用两个队列模拟一个栈的方法并适合用于实际应用，因为每一次的出栈都需要操作所有的元素，复杂度
比较高，而且两个队列只有最小队列的容量可用，比较浪费大队列的空间。
仅用于练习。
"""

from src.basic_queue import BasicQueue


class MyStack(object):
    pass

    def __init__(self, queue_a, queue_b):
        self.queue_a = queue_a
        self.queue_b = queue_b
        # 判定模拟栈最大容量为两个队列中最小的那个
        self.max_size = min(self.queue_a.max_size, self.queue_b.max_size)
        self.cur_size = 0

    def select_queue(self):
        """负责挑出当前有值队列和空队列"""

        if not self.queue_a.is_empty:
            valuable_q = self.queue_a
            empty_q = self.queue_b
        else:
            valuable_q = self.queue_b
            empty_q = self.queue_a

        return valuable_q, empty_q

    def push(self, value):
        # 如果栈当前容量大于等于最大容量，抛出栈已满异常
        if self.cur_size >= self.max_size:
            raise RuntimeError(f'当前栈{self}已满，无法入栈')

        # 否则，寻找两个队列中有数据的那个（另一为空队列用于交换数据）
        valuable_q, _ = self.select_queue()

        # 向此队列加入数据，并更新当前容量
        valuable_q.put(value)
        self.cur_size += 1

    def pop(self):
        # 如果栈当前容量为0，则抛出已空异常
        if not self.cur_size:
            raise RuntimeError(f'当前栈{self}已空，无法出栈')

        # 否则，寻找有数据的那个队列
        valuable_q, empty_q = self.select_queue()

        # 将有数据的队列中前n-1元素全部出队到另一个空队列中
        for i in range(self.cur_size - 1):
            empty_q.put(valuable_q.get())

        # 弹出第n个元素并更新当前栈容量
        element = valuable_q.get()
        self.cur_size -= 1
        return element


if __name__ == "__main__":
    # 给定两个队列，大小分别是m和n，m>n
    # 实现的栈大小是n

    q1 = BasicQueue(5)
    q2 = BasicQueue(3)

    mystack = MyStack(q1, q2)
    mystack.push(23)
    mystack.push(44)
    mystack.push(90)
    print(mystack)
    print(mystack.pop())
    print(mystack.pop())
    print(mystack.pop())
