# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的抽象工厂模式的实现程序"""


from src.factorys import (
    MysqlFactory,
    RedisFactory,
)


if __name__ == '__main__':

    # 实例化mysql的各种产品
    mysql = MysqlFactory()
    print(mysql.create_user())
    print(mysql.create_course())
    # < src.products.MysqlUser object at 0x000002013EE242E8 >
    # < src.products.MysqlCourse object at 0x000002013FE0D550 >
    

    # 实例化redis的各种产品
    redis = RedisFactory()
    print(redis.create_user())
    print(redis.create_course())
    # < src.products.RedisUser object at 0x000002013EE24390 >
    # < src.products.RedisCourse object at 0x000002013EE24390 >
