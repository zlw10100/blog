# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.objectsets import MySet



if __name__ == '__main__':
    myset = MySet(*[2,3,4,6])
    myiterator = myset.create_iterator()

    print(myiterator.first())
    print(myiterator.next())
    print(myiterator.next())
    print(myiterator.next())
    print(myiterator.next())
    print(myiterator)
    print(myiterator.cur_item())
























