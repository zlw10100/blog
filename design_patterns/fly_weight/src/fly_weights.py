# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""网站站点模块
此模块定义了多种网站站点，每一种网站站点都可以被不同的网站管理员使用(需要提供每一位管理员自己的账号)
这里假设同一类网站站点都是相似的，所以多个管理员可以共享同一个网站站点对象(实际业务场景中基本不太可能)。
"""

from abc import ABCMeta, abstractmethod


class AbstractWebSite(object, metaclass=ABCMeta):
    @abstractmethod
    def run(self, *args, **kwargs):pass


class NewsSite(AbstractWebSite):
    def run(self, *args, **kwargs):
        print('新闻网站启动, 当前内存地址:', id(self))
        print('当前用户账户是:', kwargs.get('username'))


class BlogSite(AbstractWebSite):
    def run(self, *args, **kwargs):
        print('博客网站启动, 当前内存地址:', id(self))


class MusicSite(AbstractWebSite):
    def run(self, *args, **kwargs):
        print('音乐网站启动, 当前内存地址:', id(self))


site_map = {
    'news': NewsSite(),
    'blog': BlogSite(),
    'music': MusicSite(),
}
