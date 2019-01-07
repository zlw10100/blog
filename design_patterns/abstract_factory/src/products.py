# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from abc import ABCMeta, abstractmethod

# 产品类别1
class AbstractUser(object, metaclass=ABCMeta):
    pass

# 产品类别2
class AbstractCourse(object, metaclass=ABCMeta):
    pass

# 具体产品类1
class MysqlUser(AbstractUser):
    pass

# 具体产品类1
class RedisUser(AbstractUser):
    pass

# 具体产品类2
class MysqlCourse(AbstractCourse):
    pass

# 具体产品类2
class RedisCourse(AbstractCourse):
    pass








