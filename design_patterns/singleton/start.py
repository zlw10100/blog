# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的单例模式实现程序
不论对业务类实例化多少次，均只有一个全局唯一的实例化对象，且初始化也仅执行一次。
"""


class MySingletonMeta(type):
    def __call__(self, *args, **kwargs):  # 重写元类__call__方法
        if not hasattr(self, '_singleton'):
            instance = object.__new__(self)  # 控制实例化过程
            self.__init__(instance, *args, **kwargs)  # 控制初始化过程
            setattr(self, '_singleton', instance)

        # 返回实例化对象
        instance = getattr(self, '_singleton')
        return instance


class Tool(object, metaclass=MySingletonMeta):
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    t1 = Tool('网络连接工具')
    t2 = Tool('网络连接工具')
    print(t1 is t2)  # True

    t3 = Tool('打印工具')
    print(t1 is t2 is t3)  # True
    print(t3.name)  # 网络连接工具
