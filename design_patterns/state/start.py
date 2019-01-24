# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现状态模式的程序
定义一个编程工作，并设定不同的状态以实现不同的工作行为。
"""


from src.works import ProgramWork
from src.states import (
    MorningState,
    AfterNoonState,
    EveningState,
)


if __name__ == '__main__':
    # 实例化工作对象
    pw = ProgramWork()

    # 实例化一个初始状态
    morning = MorningState()
    pw.set_state(morning)

    # 状态变化会驱动不同的执行逻辑
    pw.cur_hour = 8
    pw.work()

    pw.cur_hour = 15
    pw.work()

    pw.cur_hour = 21
    pw.work()

    # 第二天
    pw.cur_hour = 9
    pw.work()
