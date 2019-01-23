# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的用于实现享元模式的程序
此程序提供了多种网站站点对象，不同的管理员通过各自的账户使用站点对象。
对于同一种网站站点，多个管理员共用一个站点对象。

注：实际场景中，此案例并不合适用于实现享元模式。
更适合享元模式的案例是：围棋的棋子、俄罗斯方块游戏的方块。
"""


from src.web_factory import WebFactory


if __name__ == '__main__':
    factory = WebFactory()

    name = 'news'
    site = factory.get_site(name)
    site.run(username='zlw')
    # 新闻网站启动, 当前内存地址: 39771272
    # 当前用户账户是: zlw

    name = 'news'
    site = factory.get_site(name)
    site.run(username='kaka')
    # 新闻网站启动, 当前内存地址: 39771272
    # 当前用户账户是: kaka
