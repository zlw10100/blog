# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.implements import Stack


# 定义用例
if __name__ == '__main__':
    stack = Stack()
    assert stack.size() == 0, '空栈容量判定接口测试失败'
    assert stack.is_empty() is True, '空栈判空接口测试失败'
    item_list = list()
    for item in stack:
        item_list.append(item)
    assert len(item_list) == 0, '空栈迭代接口测试失败'

    stack.push(2)
    assert stack.size() == 1, '非空栈容量判定接口测试失败'
    assert stack.is_empty() is False, '非空栈判空接口测试失败'
    item = stack.pop()
    assert item == 2, '非空栈弹出接口测试失败'

    stack.push(3)
    stack.push(6)
    stack.push(9)
    item_list = list()
    for item in stack:
        item_list.append(item)
    assert item_list == [9, 6, 3], '非空栈迭代接口测试失败'

    print('测试通过')
