# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


class SingletonMeta(type):
    def __call__(self, *args, **kwargs):
        if not hasattr(self, '_singleton'):
            instance = object.__new__(self)
            self.__init__(instance, *args, **kwargs)
            setattr(self, '_singleton', instance)
        return getattr(self, '_singleton')

class Tool(object, metaclass=SingletonMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def use_tools(self):
        print('工具类的实例化对象只需要全局唯一即可。')


if __name__ == '__main__':
    t1 = Tool('zlw', 23)
    t2 = Tool('kk', 23)
    print(t1.name, t2.name)
    print(id(t1), id(t2))
    print(t1 is t2)









