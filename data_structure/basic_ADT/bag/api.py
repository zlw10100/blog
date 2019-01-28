# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


# 第一步，定义api
"""
背包api的定义。
一个集合类的抽象数据类型，只能加入元素，但无法删除元素。

class Bag:
    Bag()           实例化一个背包对象
    
    void add(item)  向背包中加入一个元素
    bool is_empty() 判断背包是否为空
    int size()      获取当前背包的容量大小
    __iter__        生成当前背包的迭代器对象
    __next__        获取当前背包中的下一个元素
"""


from implements import DefaultBag as Bag


# 第二步，定义用例
if __name__ == '__main__':
    # 背包为空
    bag = Bag()
    assert bag.is_empty() is True, '背包为空时判空接口测试失败'
    assert bag.size() == 0, '背包为空时获取当前容量接口测试失败'
    item_list = list()
    for item in bag:
        item_list.append(item)
    assert len(item_list) == 0, '背包为空时迭代接口测试失败'

    # 背包非空
    bag.add(1)
    assert bag.is_empty() is False, '背包不为空时判空接口测试失败'
    assert bag.size() == 1, '背包不为空时获取当前容量接口测试失败'
    item_list = list()
    for item in bag:
        item_list.append(item)
    assert len(item_list) == 1 and item_list[0] == 1, '背包不为空时迭代接口测试失败'

    # 最大容量动态检测
    pass

    print('测试用例通过')
