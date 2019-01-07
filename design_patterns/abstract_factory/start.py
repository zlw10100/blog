# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.factorys import (
    MysqlFactory,
    RedisFactory,
)

if __name__ == '__main__':

    # 实例化mysql的各种产品
    mysql = MysqlFactory()
    print(mysql.create_user())
    print(mysql.create_course())

    # 实例化redis的各种产品
    redis = RedisFactory()
    print(redis.create_user())
    print(redis.create_course())














