# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.cal.operations import operate_factory

class Cal():
    def cal(self, a, b, o):
        # 计算并返回结果
        result = None

        # 获取对应的操作符类
        operate_cls = operate_factory(o)
        if operate_cls is not None:
            # 如果正确就计算结果
            operate = operate_cls(a, b)
            result = operate.result

        print('结果是:', result)










