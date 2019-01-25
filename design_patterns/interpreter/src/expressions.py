# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""表达式模块
此模块定义了语言的非终止、终止表达式类。
"""


class AbstractExpression(object):
    def interpret(self, data, *args, **kwargs):
        pass


class UnterminalExpression(AbstractExpression):
    pass


class AssignmentExpression(UnterminalExpression):
    """赋值表达式类"""

    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def interpret(self, data):
        """赋值的解释接口"""

        # 判定提供了等于号(赋值含义)
        if data.count('=') != 1:
            return False, '赋值语句语法错误'

        # 判断是否提供了正确数量的变量名和值
        try:
            variable_name, variable_value = data.split('=')
        except ValueError:
            return False, '赋值语句语法错误'
        else:
            if variable_name is '' or variable_value is '':
                return False, '赋值语句语法错误'

        # 解释标识符
        variable_name = variable_name.strip()
        status, result = self.identifier.interpret(variable_name)
        if status is False:
            return False, result

        # 解释值
        variable_value = variable_value.strip()
        status, result = self.value.interpret(variable_value)
        if status is False:
            return False, result

        # 执行赋值
        try:
            exec(data)
            print('执行完毕:', data)
        except Exception as why:
            return False, f'赋值语句语法错误: {why}'

        return True, ''


class TerminalExpression(AbstractExpression):
    pass


class IdentifierExpression(TerminalExpression):
    """标识符表达式类"""

    def __init__(self, allow_char_list, allow_start_char_list, keyword_list):
        self.allow_char_list = allow_char_list
        self.allow_start_char_list = allow_start_char_list
        self.keyword_list = keyword_list

    def interpret(self, data):
        """标识符的解释接口"""

        # 判断是否为关键字
        if data in self.keyword_list:
            return False, f'标识符不能是内置关键字'

        # 判断每一个字符是否都在允许的字符列表中
        for char in data:
            if char not in self.allow_char_list:
                return False, f'标识符只能由这些字符组成: {self.allow_char_list}'

        # 判断开头字符是否在允许的开头字符列表中
        start_char = data[0]
        if start_char not in self.allow_start_char_list:
            return False, f'标识符合法的首字母为: {self.allow_start_char_list}'

        return True, ''


class ValueExpression(TerminalExpression):
    """值表达式类"""

    def interpret(self, data):
        """值判定接口"""

        # 判定值的类型
        pass

        # 如果是字符串类型，则要判定是否是合法的字符串字面量(引号配对问题)
        # 使用栈判断引号配对问题
        pass

        # 如果是非字符串，则意味着是引用，判断值是否存在于内存中
        try:
            print('try', globals())
            data = eval(data, globals())
        except NameError:
            return False, f'变量{data}未定义'

        return True, ''

