# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod
# 元素类代表着数据
class AbstractElement(object, metaclass=ABCMeta):
    # 每一个数据元素都需要接受一个访问者(操作对象)来操作自己
    @abstractmethod
    def accept(self, visitor): pass

# 具体的元素类
# 注意：男人可以被多个算法对象访问，我们可以灵活的增加算法对象
# 但是男人和女人这两种数据结构（或者说对象）必须稳定
class Man(AbstractElement):
    # 男人数据类要接受一个访问者的访问
    def accept(self, visitor):
        # 访问者调用对应的方法访问男人对象
        visitor.visitor_man(self)

class Woman(AbstractElement):
    def accept(self, visitor):
        visitor.visitor_woman(self)




























