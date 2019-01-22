# -*- coding: utf-8 -*-
# 'author':'zlw'


"""
使用双向循环链表作为底层数据结构，提供缓存功能
如果一定要使用递归的方式来处理斐波那契数列计算，
计算过程涉及非常多的重复计算，可以使用缓存来实现。
1  1  2  3  5  8  13...

在不考虑缓存空间大小的情况下，使用字典来保存中间计算结果，
缓存查询的复杂度是O(1)，但是需要花费大量空间。

在考虑缓存空间大小的情况下，使用链表来模拟缓存空间。
每次先通过O(n)的复杂度查询链表中是否有此结果，
如果有，则弹出此结果并加入到头结点。
如果没有，则计算结果并
判断链表是否已满，不是的话则 加入到头结点。
否则，弹出尾节点
这种处理方式可以将最新的数据保存在头结点，数据新鲜度向右依次递减

使用一个字典来保存计算结果节点的索引值，这样缓存搜索就只需要O(1)
然后使用单向链表来保存计算的结果值，即可以使用高速的缓存查询又可以约束空间大小。

python的lru_cache装饰器
"""


from src.doublecycle_linkedlist import ListNode, DoubleCycleLinkedList


class LRUCache(object):
    """
    缓存类，封装底层链表结构
    缓存将(索引，值)的形式将数据存入链表中
    """

    node_class = ListNode

    def __init__(self, max_size=128):
        self.max_size = max_size
        self.cur_size = 0

        # 使用链表
        self.link = DoubleCycleLinkedList()

    def get(self, key):
        target_value = None
        for i, node in enumerate(self.link.traverse_each()):
            k, v = node.value
            if k == key: # hit
                target_value = v
                # 移动该节点到头部位置
                self.link.append_left(self.link.pop(i))
        return target_value

    def save(self, key, value):
        data = (key, value)
        node = self.node_class(data)

        # 判断当前缓存是否已满
        pop_size = self.cur_size - self.max_size + 1
        if pop_size > 0:
            # 如果已满，则剔除新鲜度最低的元素
            for i in range(pop_size):
                self.link.pop()
                self.cur_size -= 1

        # 将数据加入缓存
        self.link.append_left(node)
        self.cur_size += 1
        print(self.link)


cache = LRUCache(10)

def fib(n):
    if n < 3:
        return 1
    else:
        # 判断缓存是否有
        result = cache.get(n)
        if result:
            return result
        else:
            result = fib(n - 1) + fib(n - 2)
            cache.save(n, result)
            return result


if __name__ == '__main__':
    print(fib(400))
