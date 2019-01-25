# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现访问者模式的程序
此程序模拟不同角色对账本数据的访问。
"""


from src.object_structures import AccountBook
from src.elements import (
    Income,
    Pay,
)
from src.visitors import (
    Boss,
    Manager,
    Cashier,
)


if __name__ == '__main__':
    # 实例化元素对象
    income = Income()
    pay = Pay()

    # 实例化对象结构
    account_book = AccountBook()
    # 对象结构增加元素对象(为了可以遍历展示访问结果)
    account_book.add(income)
    account_book.add(pay)

    # 实例化访问者
    boss = Boss()
    manager = Manager()
    cashier = Cashier()

    # 展示访问者对所有元素对象的访问结果
    account_book.accept(boss)
    account_book.accept(manager)
    account_book.accept(cashier)

    # 也可以针对某一个元素对象执行访问
    pay.accept(manager)
