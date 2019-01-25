# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""上下文模块
此模块定义了上下文类的行为。
"""


class AssignmentContext(object):
    def __init__(self, assignment, global_dict):
        self.assignment = assignment
        self.global_dict = global_dict

    def execute(self, sentence):
        status, result = self.assignment.interpret(sentence, self.global_dict)
        if status is False:
            print('赋值执行失败，原因是:', result)
