# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

# 指挥官，要求每一个建造者必须调用固定构造方法
class Commander(object):
    # 驱动建造者启动构造行为
    def drive_construct(self, builder):
        builder.build_base()
        builder.build_wall()










