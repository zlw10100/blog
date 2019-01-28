# !/usr/bin/python
# -*- coding:utf-8 -*-


# 第一步，定义api
"""
队列api定义：
一个支持先进先出的集合。

class Queue<Item>:
    Queue()                     实例化一个队列对象

    void enqueue(Item item)     将元素入队
    Item dequeue()              出队元素
    bool is_empty()             队列判空
    int size()                  返回队列当前容量
    __iter__                    返回队列迭代器对象
    __next__                    返回迭代器中下一个元素
"""


from implements import DefaultQueue as Queue


# 第二步，定义用例
if __name__ == '__main__':
    queue = Queue()
    assert queue.size() == 0, '空队列容量接口测试失败'
    assert queue.is_empty() is True, '空队列判空接口测试失败'
    item_list = list()
    for item in queue:
        item_list.append(item)
    assert item_list == [], '空队列迭代接口测试失败'

    queue.enqueue(2)
    queue.enqueue(6)
    queue.enqueue(10)
    item = queue.dequeue()
    assert item == 2, '非空队列出队接口测试失败'
    item_list = list()
    for item in queue:
        item_list.append(item)
    assert item_list == [6, 10], '非空队列迭代接口测试失败'

    print('测试通过')

    for i in queue:
        print(i)
    print(queue.max_size)
    queue.enqueue(9)
    queue.enqueue(9)
    queue.enqueue(9)
    queue.enqueue(9)
    print('max size', queue.max_size)
    for i in queue:
        print('i是:', i)
    print(queue.max_size)
    print(queue.size())
    print(queue.dequeue())
    print('11', queue.size())
    print(queue.max_size)
    print(queue.dequeue())
    print('11', queue.size())
    print(queue.max_size)
    print(queue.dequeue())
    print(queue.max_size)

