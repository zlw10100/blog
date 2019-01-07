# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.object_structure import ObjectStructure
from src.elements import (
    Man,
    Woman,
)
from src.visitors import (
    HandleA,
    HandleB,
)


if __name__ == '__main__':
    # 实例化元素对象
    man = Man()
    woman = Woman()

    # 实例化对象结构对象（其实就是一个管理者）
    obj_struct = ObjectStructure()

    # 对象结构增加元素对象(为了可以遍历展示访问结果)
    obj_struct.attach(man)
    obj_struct.attach(woman)

    # 实例化算法1
    handle_a = HandleA()

    # 展示算法1对所有元素对象的访问结果
    obj_struct.accept(handle_a)

    # 实例化算法2
    handle_b = HandleB()

    # 展示算法2对所有元素对象的访问结果
    obj_struct.accept(handle_b)

    # 展示算法2对某一个元素对象的访问结果
    man.accept(handle_b)







