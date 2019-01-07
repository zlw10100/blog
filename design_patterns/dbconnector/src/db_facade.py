# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from src.db_connectors import (
    FileDB,
    JsonFileDB,
    MySqlDB,
    RedisDB,
)


db_map = {
    'file': FileDB(),
    'json': JsonFileDB(),
    'mysql': MySqlDB(),
    'redis': RedisDB(),
}

# 数据库门面模式，提供统一访问接口的抽象层
class DBFacade(object):
    def __init__(self, db_name):
        self.db = db_map.get(db_name)
        
    def save(self, data):
        return self.db.save(data)
    
    











