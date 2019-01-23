# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""指挥官模块
此模块为用户提供了一个统一管理的接口，为用户驱动每一个建造者的建造过程。
"""


# 指挥官，要求每一个建造者必须调用固定构造方法
class Commander(object):
    def drive_construct(self, builder):  # 驱动建造者启动构造行为
        builder.build_base()
        builder.build_wall()
