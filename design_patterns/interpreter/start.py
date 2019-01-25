# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25



"""
模拟对python赋值语句的解释
<赋值语句> ::= <标识符> = <值>
1. 解析语句判断合法性
2. 得到语句的结果
"""


import string

from src.contexts import AssignmentContext
from src.expressions import (
    AssignmentExpression,
    IdentifierExpression,
    ValueExpression,
)


if __name__ == '__main__':
    # 定义标识符合法数据且实例化标识符表达式
    identifier = IdentifierExpression(
        allow_char_list=string.ascii_letters + string.digits + '_',
        allow_start_char_list=string.ascii_letters + '_',
        keyword_list=['if', 'else', 'def', 'class'],  # 关键字列表，此处仅列出部分
    )

    # 实例化值表达式
    value = ValueExpression()

    # 实例化赋值表达式
    assignment = AssignmentExpression(identifier, value)

    # 实例化赋值上下文
    context = AssignmentContext(assignment, globals())

    # 使用上下文解释赋值语句
    # sentence = 'if = 2'
    # context.execute(sentence)
    # 赋值执行失败，原因是: 标识符不能是内置关键字

    sentence = '0a = 2'
    context.execute(sentence)
    # 赋值执行失败，原因是: 标识符合法的首字母为: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_

    sentence = 'a?b = 2'
    context.execute(sentence)
    # 赋值执行失败，原因是: 标识符只能由这些字符组成: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_

    result = 103
    print(globals())
    print(globals()['result'])
    sentence = 'a = result'
    context.execute(sentence)
    # print(a)



