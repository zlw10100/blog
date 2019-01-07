# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


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




