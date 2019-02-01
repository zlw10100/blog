# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/2/1


"""固长环形队列用例"""


from src.implements import RingQue


if __name__ == '__main__':
    buffer = RingQue(max_size=5)

    # 加入缓冲区
    buffer.enqueue(1)
    buffer.enqueue(2)
    buffer.enqueue(3)
    buffer.enqueue(4)
    buffer.enqueue(5)
    print(buffer.is_full())
    print(buffer.size())

    # 离开缓冲区
    print(buffer.dequeue())
    print(buffer.dequeue())
    print(buffer.dequeue())
    print(buffer.dequeue())
    print(buffer.dequeue())
    print(buffer.is_empty())
    print(buffer.size())
