# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现迭代器模式的程序
程序模拟一个数组的迭代行为。
"""


from src.sets import MySet


if __name__ == '__main__':
    myset = MySet(*[2,3,4,6])
    myiterator = myset.create_iterator()

    print(myiterator.first())
    # 2
    print(myiterator.next())
    # 3
    print(myiterator.next())
    # 4
    print(myiterator.next())
    # 6
    print(myiterator.next())
    # None
    print(myiterator)
    # < src.iterators.MyIterator object at 0x00000000021C8978 >
    print(myiterator.cur_item())
    # 6
