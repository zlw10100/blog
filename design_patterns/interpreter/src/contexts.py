# !/usr/bin/python
# -*- coding:utf-8 -*-


"""上下文模块
此模块定义了上下文类的行为。
"""


class AssignmentContext(object):
    def __init__(self, assignment):
        self.assignment = assignment

    def execute(self, sentence):
        status, result = self.assignment.interpret(sentence)
        if status is False:
            print('赋值执行失败，原因是:', result)
