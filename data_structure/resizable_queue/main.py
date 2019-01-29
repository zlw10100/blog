# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/29


from src.implements import RQueue


# 定义用例
if __name__ == '__main__':
    q = RQueue(fixed_size=None)
    print(list(q))
    q.enqueue('hello')
    print(list(q))
    q.enqueue('word')
    print(list(q))

    q.enqueue(23)
    print(list(q))
    print(q.dequeue())
    print(list(q))
    q.enqueue(99)
    q.enqueue(True)
    q.enqueue('你好')

    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(list(q))

    q = RQueue(fixed_size=4)
    q.enqueue(22)
    q.enqueue(33)
    q.enqueue(44)
    q.enqueue(55)

    q.dequeue()
    q.enqueue('abc')
    print(list(q))
