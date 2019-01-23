# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现组合模式的程序"""


from src.compoents import Composite, Leave


if __name__ == '__main__':
    # 定义根结点
    root = Composite('root')
    # 定义叶子节点
    leave_a = Leave('leave_a')
    leave_b = Leave('leave_b')
    root.add(leave_a)
    root.add(leave_b)

    # 定义一个树枝节点
    comp = Composite('comp')
    # 定义叶子节点
    comp_left = Leave('comp_left')
    comp_right = Leave('comp_right')
    comp.add(comp_left)
    comp.add(comp_right)

    # 嫁接另一个树枝节点
    root.add(comp)

    # 查看此节点下的所有节点信息
    root.display(1)
    # = root Composite
    # == leave_a Leave
    # == leave_b Leave
    # == comp Composite
    # === comp_left Leave
    # === comp_right Leave
