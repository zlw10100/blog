# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


class BaseDB(object):
    def save(self, data):
        print('当前使用的数据库是:', type(self).__name__)
        print('保存数据:', data)


# 每一个数据库类负责连接对应的存储，并实现数据的相关操作
class FileDB(BaseDB):
    pass


class JsonFileDB(BaseDB):
    pass


class MySqlDB(BaseDB):
    pass


class RedisDB(BaseDB):
    pass













