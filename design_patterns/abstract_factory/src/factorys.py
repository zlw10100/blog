# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from abc import ABCMeta, abstractmethod

from src.products import (
    MysqlUser,
    MysqlCourse,
    
    RedisUser,
    RedisCourse,
)

# 抽象工厂类
class AbstractFactory(object, metaclass=ABCMeta):
    # 每一个工厂都要有两个产品的实例化行为
    @abstractmethod
    def create_user(self): pass
    
    @abstractmethod
    def create_course(self): pass


# 具体工厂类
class MysqlFactory(AbstractFactory):
    def create_user(self):
        return MysqlUser()
    
    def create_course(self):
        return MysqlCourse()


class RedisFactory(AbstractFactory):
    def create_user(self):
        return RedisUser()
    
    def create_course(self):
        return RedisCourse()






