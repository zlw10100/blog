# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/2/1


"""固长环形队列api定义"""


from abc import ABCMeta, abstractmethod


class AbstractFixedRingQue(object, metaclass=ABCMeta):
    @abstractmethod
    def enqueue(self, item):
        """入队接口

        若队列未满，则将指定的元素加入队列。
        若队列满，将会抛出已满异常。

        返回：
            入队成功时返回None
            入队失败时返回已满异常
        """
        pass

    @abstractmethod
    def dequeue(self):
        """出队接口

        若队列未空，则返回最先加入的元素。
        若队列已空，将会抛出已空异常。

        返回：
            出队成功时返回最先加入的元素
            出队失败时返回已空异常
            """
        pass

    @abstractmethod
    def is_empty(self):
        """判空接口

        若当前队列已空，则返回True否则返回False
        """
        pass

    @abstractmethod
    def is_full(self):
        """判满接口

        若当前队列已满，则返回True否则返回False
        """
        pass

    @abstractmethod
    def size(self):
        """判容接口

        返回队列当前的int型有效长度
        """
        pass

    @abstractmethod
    def __iter__(self):
        """迭代器创建接口

        返回一个迭代器。
        """
        pass

    @abstractmethod
    def __next__(self):
        """迭代接口

        返回迭代器中下一个元素。
        """
        pass


class Error(Exception):
    pass


class QueIsEmptyError(Error):
    pass


class QueIsFullError(Error):
    pass
