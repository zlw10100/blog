# -*- coding: utf-8 -*-
# 'author': 'zlw'


"""
用两个栈模拟队列的效果
注意：
虽然两个栈可以模拟一个队列的FIFO效果，但是这样的实现并不适合真正应用。
这种实现只适合用于练习和锻炼逻辑，因为：

1、需要设计两套api。
如果两个栈一大一小，就会出现两种情况，数据先入大栈还是先入小栈，两种
情况涉及两套不同的逻辑（虽然差别不大）但是依然要设计两套api，很麻烦。

2、队列的最大容量无法保证。
只有当每一次入队和出队都是完全入队和完全出队才能达到最大容量（先入
大栈是2n + 1，先入小栈是2n），实际应用中无法严格做到一定要全出队或者
一定要全入队，所以不适合实际应用。

3、逻辑理解困难。
虽然两个栈可以通过两次倒换将数据变成原来的序列，但是这种实现的逻辑比较困难，
我们应该直接使用一个单链表来实现队列，理解和实现起来都更加简单，没必要搞的
这么复杂。
"""


from src.basic_stack import BasicStack


class MyQueue(object):
    def __init__(self, primary_stack, second_stack):
        """使用两个栈模拟队列"""
        self.primary_stack = primary_stack
        self.second_stack = second_stack

    @property
    def length(self):
        pass

    def put(self, value):
        """入队接口，使用两个栈来模拟 """
        if self.primary_stack.max_size > self.second_stack.max_size:
            return self.put_bigger(value)
        else:
            return self.put_smaller(value)

    def get(self):
        if self.primary_stack.max_size > self.second_stack.max_size:
            return self.get_bigger()
        else:
            return self.get_smaller()

    def put_bigger(self, value):
        max_size = self.second_stack.max_size
        if self.primary_stack.length >= max_size:
            # 大的栈已满
            if self.second_stack.is_full:
                # 大小栈全满，队列容量上限
                if self.primary_stack.length == max_size:
                    # 还可以偷偷加一个
                    self.primary_stack.push(value)
                    print('偷偷加一个', value)
                    # 一定要结束函数
                    return
                else:
                    raise RuntimeError(f'队列{self}已满，无法入队')
            # 判断小栈是否为空，如果是则把大栈弹出到小栈
            elif self.second_stack.is_empty:
                for i in range(max_size):
                    # 把大的栈全部弹出到小的栈
                    self.second_stack.push(self.primary_stack.pop())
            else:
                # 小栈不满，但是也不空,小栈有值的时候不能弹出到小栈
                raise RuntimeError(f'队列{self}已满，无法入队')

        # 大的未满 大的栈还可以放入
        self.primary_stack.push(value)

    def get_bigger(self):
        # 首先判断小栈是否为空，如果是则将大栈弹出到小栈中
        if self.second_stack.is_empty:
            if self.primary_stack.is_empty:
                raise RuntimeError(f'当前队列{self}为空，无法出队')
            else:
                i = 0
                while not self.primary_stack.is_empty:
                    value = self.primary_stack.pop()
                    i += 1
                    # 判断如果是全满情况下大栈最后弹出的多1的容量元素
                    if i == (self.second_stack.max_size + 1):
                        return value
                    else:
                        self.second_stack.push(value)
                # 弹出小栈栈顶数据
                return self.second_stack.pop()
        else:
            # 否则弹出小栈的数据
            return self.second_stack.pop()

    def put_smaller(self, value):
        # 如果小栈不满，则放入小栈
        if not self.primary_stack.is_full:
            self.primary_stack.push(value)
        else:
            # 如果小栈满，判断大栈
            # 如果大栈为空，则弹出到大栈，
            if self.second_stack.is_empty:
                while not self.primary_stack.is_empty:
                    self.second_stack.push(self.primary_stack.pop())
                self.primary_stack.push(value)
            else:
                # 否则，抛出已满
                raise RuntimeError(f'当前队列{self}已满，无法入队')

    def get_smaller(self):
        # 首先获取大栈，如果大栈空了
        if self.second_stack.is_empty:
            if self.primary_stack.is_empty:
                raise RuntimeError(f'当前队列{self}已空，无法出队')
            else:
                # 把小栈的弹出到大栈，然后弹出一个大栈元素
                while not self.primary_stack.is_empty:
                    self.second_stack.push(self.primary_stack.pop())
                return self.second_stack.pop()
        else:
            # 如果大栈未空，则弹出大栈
            return self.second_stack.pop()


if __name__ == "__main__":
    # 如果两个栈一大一小，大栈容量m，小栈容量n，则：
    # 若优先使用小栈，则队列容量为2n
    # 若优先使用大栈，则队列容量为2n + 1
    primary_stack = BasicStack(max_size=8)
    second_stack = BasicStack(max_size=5)

    q = MyQueue(primary_stack, second_stack)
    for i in range(15):
        try:
            q.put(i)
            print(f'当前已经入队: {i} , 入队数量: {i + 1}')
        except RuntimeError as why:
            break

    for e in primary_stack._traverse_each():
        print(e.value)

    print('=')

    for e in second_stack._traverse_each():
        print(e.value)

    for i in range(15):
        try:
            v = q.get()
            print(f'当前已经出队: {v}, 出队数量: {i + 1}')
        except RuntimeError as why:
            break

    # primary_stack = BasicStack(max_size=3)
    # second_stack = BasicStack(max_size=8)

    # q = MyQueue(primary_stack, second_stack)
    # for i in range(15):
    #     try:
    #         q.put(i)
    #         print(f'当前已经入队: {i} , 入队数量: {i + 1}')
    #     except RuntimeError as why:
    #         print(why)
    #         break

    # for e in primary_stack._traverse_each():
    #     print(e.value)

    # print('=')

    # for e in second_stack._traverse_each():
    #     print(e.value)

    # for i in range(10):
    #     try:
    #         v = q.get()
    #         print(f'当前已经出队: {v}, 出队数量: {i + 1}')
    #     except RuntimeError as why:
    #         print(why)
    #         break
