# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.implements import Queue


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
