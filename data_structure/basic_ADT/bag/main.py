# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.implements import Bag


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

    # 查看背包的数据
    bag.add('hello')
    bag.add('world')
    item_list = bag.iter_item()
    print(item_list)

    # 最大容量动态检测
    pass

    print('测试用例通过')
